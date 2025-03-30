import dataclasses
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Iterable, Iterator, Literal, Sequence

from frozendict import frozendict

from . import set_operations
from .node_types import NodeData, RootNodeData
from .tree_formatters import (
    HTML,
    node_tree_to_html,
    node_tree_to_string,
)
from .value_types import QEnum, ValueGroup, WildcardGroup, values_from_json


@dataclass(frozen=False, eq=True, order=True, unsafe_hash=True)
class Qube:
    data: NodeData
    children: tuple["Qube", ...]

    @property
    def key(self) -> str:
        return self.data.key

    @property
    def values(self) -> ValueGroup:
        return self.data.values

    @property
    def metadata(self) -> frozendict[str, Any]:
        return self.data.metadata

    def replace(self, **kwargs) -> "Qube":
        data_keys = {
            k: v for k, v in kwargs.items() if k in ["key", "values", "metadata"]
        }
        node_keys = {k: v for k, v in kwargs.items() if k == "children"}
        if not data_keys and not node_keys:
            return self
        if not data_keys:
            return dataclasses.replace(self, **node_keys)

        return dataclasses.replace(
            self, data=dataclasses.replace(self.data, **data_keys), **node_keys
        )

    def summary(self) -> str:
        return self.data.summary()

    @classmethod
    def make(cls, key: str, values: ValueGroup, children, **kwargs) -> "Qube":
        return cls(
            data=NodeData(key, values, metadata=kwargs.get("metadata", frozendict())),
            children=tuple(sorted(children, key=lambda n: ((n.key, n.values.min())))),
        )

    @classmethod
    def root_node(cls, children: Iterable["Qube"]) -> "Qube":
        return cls.make("root", QEnum(("root",)), children)

    @classmethod
    def from_datacube(cls, datacube: dict[str, str | Sequence[str]]) -> "Qube":
        key_vals = list(datacube.items())[::-1]

        children: list["Qube"] = []
        for key, values in key_vals:
            if values == "*":
                values = WildcardGroup()
            elif not isinstance(values, list):
                values = [values]

            if isinstance(values, list):
                values = QEnum(values)

            children = [cls.make(key, values, children)]

        return cls.root_node(children)

    @classmethod
    def from_json(cls, json: dict) -> "Qube":
        def from_json(json: dict) -> Qube:
            return Qube.make(
                key=json["key"],
                values=values_from_json(json["values"]),
                metadata=frozendict(json["metadata"]) if "metadata" in json else {},
                children=(from_json(c) for c in json["children"]),
            )

        return from_json(json)

    def to_json(self) -> dict:
        def to_json(node: Qube) -> dict:
            return {
                "key": node.key,
                "values": node.values.to_json(),
                "metadata": dict(node.metadata),
                "children": [to_json(c) for c in node.children],
            }

        return to_json(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Qube":
        def from_dict(d: dict) -> Iterator[Qube]:
            for k, children in d.items():
                key, values = k.split("=")
                values = values.split("/")
                if values == ["*"]:
                    values = WildcardGroup()
                else:
                    values = QEnum(values)

                yield Qube.make(
                    key=key,
                    values=values,
                    children=from_dict(children),
                )

        return Qube.root_node(list(from_dict(d)))

    @classmethod
    def from_tree(cls, tree_str):
        lines = tree_str.splitlines()
        stack = []
        root = {}

        initial_indent = None
        for line in lines:
            if not line.strip():
                continue
            # Remove tree characters and measure indent level
            stripped = line.lstrip(" │├└─")
            indent = (len(line) - len(stripped)) // 4
            if initial_indent is None:
                initial_indent = indent
            indent = indent - initial_indent

            # Split multiple key=value parts into nested structure
            keys = [item.strip() for item in stripped.split(",")]
            current = bottom = {}
            for key in reversed(keys):
                current = {key: current}

            # Adjust the stack to current indent level
            # print(len(stack), stack)
            while len(stack) > indent:
                stack.pop()

            if stack:
                # Add to the dictionary at current stack level
                parent = stack[-1]
                key = list(current.keys())[0]
                if key in parent:
                    raise ValueError(
                        f"This function doesn't yet support reading in uncompressed trees, repeated key is {key}"
                    )
                parent[key] = current[key]
            else:
                # Top level
                key = list(current.keys())[0]
                if root:
                    raise ValueError(
                        f"This function doesn't yet support reading in uncompressed trees, repeated key is {key}"
                    )
                root = current[key]

            # Push to the stack
            stack.append(bottom)

        return cls.from_dict(root)

    @classmethod
    def empty(cls) -> "Qube":
        return Qube.root_node([])

    def __str__(self, depth=None, name=None) -> str:
        node = (
            dataclasses.replace(
                self,
                data=RootNodeData(key=name, values=self.values, metadata=self.metadata),
            )
            if name is not None
            else self
        )
        return "".join(node_tree_to_string(node=node, depth=depth))

    def print(self, depth=None, name: str | None = None):
        print(self.__str__(depth=depth, name=name))

    def html(self, depth=2, collapse=True, name: str | None = None) -> HTML:
        node = (
            dataclasses.replace(
                self,
                data=RootNodeData(key=name, values=self.values, metadata=self.metadata),
            )
            if name is not None
            else self
        )
        return HTML(node_tree_to_html(node=node, depth=depth, collapse=collapse))

    def _repr_html_(self) -> str:
        return node_tree_to_html(self, depth=2, collapse=True)

    # Allow "key=value/value" / qube to prepend keys
    def __rtruediv__(self, other: str) -> "Qube":
        key, values = other.split("=")
        values = QEnum((values.split("/")))
        return Qube.root_node([Qube.make(key, values, self.children)])

    def __or__(self, other: "Qube") -> "Qube":
        return set_operations.operation(
            self, other, set_operations.SetOperation.UNION, type(self)
        )

    def __and__(self, other: "Qube") -> "Qube":
        return set_operations.operation(
            self, other, set_operations.SetOperation.INTERSECTION, type(self)
        )

    def __sub__(self, other: "Qube") -> "Qube":
        return set_operations.operation(
            self, other, set_operations.SetOperation.DIFFERENCE, type(self)
        )

    def __xor__(self, other: "Qube") -> "Qube":
        return set_operations.operation(
            self, other, set_operations.SetOperation.SYMMETRIC_DIFFERENCE, type(self)
        )

    def leaves(self) -> Iterable[dict[str, str]]:
        for value in self.values:
            if not self.children:
                yield {self.key: value}
            for child in self.children:
                for leaf in child.leaves():
                    if self.key != "root":
                        yield {self.key: value, **leaf}
                    else:
                        yield leaf

    def leaf_nodes(self) -> "Iterable[tuple[dict[str, str], Qube]]":
        for value in self.values:
            if not self.children:
                yield ({self.key: value}, self)
            for child in self.children:
                for leaf in child.leaf_nodes():
                    if self.key != "root":
                        yield ({self.key: value, **leaf[0]}, leaf[1])
                    else:
                        yield leaf

    def leaves_with_metadata(
        self, indices=()
    ) -> Iterable[tuple[dict[str, str], dict[str, str]]]:
        if self.key == "root":
            for c in self.children:
                for leaf in c.leaves_with_metadata(indices=()):
                    yield leaf
            return

        for index, value in enumerate(self.values):
            # print(self.key, index, indices, value)
            # print({k: np.shape(v) for k, v in self.metadata.items()})
            indexed_metadata = {
                k: vs[indices + (index,)] for k, vs in self.metadata.items()
            }
            indexed_metadata = {
                k: v.item() if v.shape == () else v for k, v in indexed_metadata.items()
            }
            if not self.children:
                yield {self.key: value}, indexed_metadata

            for child in self.children:
                for leaf, metadata in child.leaves_with_metadata(
                    indices=indices + (index,)
                ):
                    if self.key != "root":
                        yield {self.key: value, **leaf}, metadata | indexed_metadata
                    else:
                        yield leaf, metadata

    def datacubes(self) -> "Qube":
        def to_list_of_cubes(node: Qube) -> Iterable[Qube]:
            if not node.children:
                yield node
            # print(node.key)
            for c in node.children:
                # print(c)
                for sub_cube in to_list_of_cubes(c):
                    yield node.replace(children=[sub_cube])

        return Qube.root_node((q for c in self.children for q in to_list_of_cubes(c)))

    def __getitem__(self, args) -> "Qube":
        if isinstance(args, str):
            specifiers = args.split(",")
            current = self
            for specifier in specifiers:
                key, values = specifier.split("=")
                values = values.split("/")
                for c in current.children:
                    if c.key == key and set(values) == set(c.values):
                        current = c
                        break
                else:
                    raise KeyError(
                        f"Key '{key}' not found in children of '{current.key}', available keys are {[c.key for c in current.children]}"
                    )
            return Qube.root_node(current.children)

        elif isinstance(args, tuple) and len(args) == 2:
            key, value = args
            for c in self.children:
                if c.key == key and value in c.values:
                    return Qube.root_node(c.children)
            raise KeyError(f"Key {key} not found in children of {self.key}")
        else:
            raise ValueError("Unknown key type")

    @cached_property
    def n_leaves(self) -> int:
        # This line makes the equation q.n_leaves + r.n_leaves == (q | r).n_leaves true is q and r have no overlap
        if self.key == "root" and not self.children:
            return 0
        return len(self.values) * (
            sum(c.n_leaves for c in self.children) if self.children else 1
        )

    @cached_property
    def n_nodes(self) -> int:
        if self.key == "root" and not self.children:
            return 0
        return 1 + sum(c.n_nodes for c in self.children)

    def transform(self, func: "Callable[[Qube], Qube | Iterable[Qube]]") -> "Qube":
        """
        Call a function on every node of the Qube, return one or more nodes.
        If multiple nodes are returned they each get a copy of the (transformed) children of the original node.
        Any changes to the children of a node will be ignored.
        """

        def transform(node: Qube) -> list[Qube]:
            children = tuple(sorted(cc for c in node.children for cc in transform(c)))
            new_nodes = func(node)
            if isinstance(new_nodes, Qube):
                new_nodes = [new_nodes]

            return [new_node.replace(children=children) for new_node in new_nodes]

        children = tuple(cc for c in self.children for cc in transform(c))
        return self.replace(children=children)

    def convert_dtypes(self, converters: dict[str, Callable[[Any], Any]]):
        def convert(node: Qube) -> Qube:
            if node.key in converters:
                converter = converters[node.key]
                new_node = node.replace(values=QEnum(map(converter, node.values)))
                return new_node
            return node

        return self.transform(convert)

    def select(
        self,
        selection: dict[str, str | list[str] | Callable[[Any], bool]],
        mode: Literal["strict", "relaxed"] = "relaxed",
        prune=True,
        consume=False,
    ) -> "Qube":
        # make all values lists
        selection: dict[str, list[str] | Callable[[Any], bool]] = {
            k: v if isinstance(v, list | Callable) else [v]
            for k, v in selection.items()
        }

        def not_none(xs):
            return tuple(x for x in xs if x is not None)

        def select(node: Qube, selection: dict[str, list[str]]) -> Qube | None:
            # If this node has no children but there are still parts of the request
            # that have not been consumed, then prune this whole branch
            if consume and not node.children and selection:
                return None

            # If the key isn't in the selection then what we do depends on the mode:
            # In strict mode we just stop here
            # In next_level mode we include the next level down so you can tell what keys to add next
            # In relaxed mode we skip the key if it't not in the request and carry on
            if node.key not in selection:
                if mode == "strict":
                    return None

                # If this node doesn't exist in the
                elif mode == "next_level":
                    return node.replace(
                        children=(),
                        metadata=self.metadata | {"is_leaf": not bool(self.children)},
                    )

                elif mode == "relaxed":
                    pass
                else:
                    raise ValueError(f"Unknown mode argument {mode}")

            # If the key IS in the selection then check if the values match
            if node.key in selection:
                # If the key is specified, check if any of the values match
                selection_criteria = selection[node.key]
                if isinstance(selection_criteria, Callable):
                    values = QEnum((c for c in node.values if selection_criteria(c)))
                else:
                    values = QEnum((c for c in selection[node.key] if c in node.values))

                # Here modes don't matter because we've explicitly filtered on this key and found nothing
                if not values:
                    return None

                node = node.replace(values=values)

            if consume:
                selection = {k: v for k, v in selection.items() if k != node.key}

            # Prune nodes that had had all their children pruned
            new_children = not_none(select(c, selection) for c in node.children)
            # if node.key == "dataset": print(prune, [(c.key, c.values.values) for c in node.children], [c.key for c in new_children])

            if prune and node.children and not new_children:
                return None

            return node.replace(
                children=new_children,
                metadata=self.metadata | {"is_leaf": not bool(new_children)},
            )

        return self.replace(
            children=not_none(select(c, selection) for c in self.children)
        )

    def span(self, key: str) -> list[str]:
        """
        Search the whole tree for any value that a given key takes anywhere.
        """
        this = set(self.values) if self.key == key else set()
        return sorted(this | set(v for c in self.children for v in c.span(key)))

    def axes(self) -> dict[str, set[str]]:
        """
        Return a dictionary of all the spans of the keys in the qube.
        """
        axes = defaultdict(set)
        for c in self.children:
            for k, v in c.axes().items():
                axes[k].update(v)
        if self.key != "root":
            axes[self.key].update(self.values)
        return dict(axes)

    @cached_property
    def structural_hash(self) -> int:
        """
        This hash takes into account the key, values and children's key values recursively.
        Because nodes are immutable, we only need to compute this once.
        """

        def hash_node(node: Qube) -> int:
            return hash(
                (node.key, node.values, tuple(c.structural_hash for c in node.children))
            )

        return hash_node(self)

    def compress(self) -> "Qube":
        # First compress the children (this recursively compresses all the way to the leaves)
        new_children = [child.compress() for child in self.children]

        # Now compress the set of children at this level
        new_children = set_operations.compress_children(new_children)

        # Return the now compressed node
        return Qube.make(self.key, self.values, new_children)
