#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint


class CompressedNode:
    def __init__(
        self, class_name=None, node_id=-1, links=None, module=None, name=None
    ) -> None:

        self.class_name = class_name
        self.node_id = node_id
        self.links = links
        self.module = module
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name} ({id(self)})"

    def __eq__(self, other) -> bool:
        if isinstance(other, CompressedNode):
            return self.class_name == other.class_name

    def __hash__(self) -> int:
        return hash(self.class_name)


class CompressedTree:
    def __init__(self, composition) -> None:

        for k in composition:
            if k["module"].class_name == "Home":
                self.root = k["module"]
        self.composition = composition

        self.leaves = []
        self.tree = {}

    def chain(self) -> None:

        self.compressed = {e["module"]: e["elements"] for e in self.composition}

    def __get_children(self, node) -> list:

        for parent in self.compressed:
            if parent == node:
                return [
                    CompressedNode(
                        class_name=i.class_name,
                        node_id=i.node_id,
                        links=i.links,
                        module=i.module,
                        name=i.name,
                    )
                    for i in self.compressed[parent]
                ]

        return []

    def __decompress(self, node) -> dict:
        return {node: [self.__decompress(n) for n in self.__get_children(node)]}

    def decompress(self) -> dict:
        self.tree = self.__decompress(self.root)

    def get_tree(self) -> dict:

        return self.tree

    def __get_leaves(self, subtree) -> None:
        for key, value in subtree.items():
            if type(value) is list:
                if not value:
                    self.leaves.append(key)

                for i in value:
                    self.__get_leaves(i)

    def get_leaves(self) -> list:

        self.__get_leaves(self.tree)
        return self.leaves


example_comp = [
    {
        "elements": [
            CompressedNode(
                class_name="eight",
                node_id=13,
                links=[],
                module="Home",
                name="eight#0",
            )
        ],
        "module": CompressedNode("Home", name="root"),
    },
    {
        "elements": [
            CompressedNode(
                class_name="fulladder",
                node_id=3,
                links=[],
                module="two",
                name="fulladder#0",
            ),
            CompressedNode(
                class_name="fulladder",
                node_id=4,
                links=[],
                module="two",
                name="fulladder#1",
            ),
        ],
        "module": CompressedNode("two"),
    },
    {
        "elements": [
            CompressedNode(
                class_name="two", node_id=7, links=[], module="four", name="two#0"
            ),
            CompressedNode(
                class_name="two",
                node_id=8,
                links=[{"from_port": "cout__4", "to_id": 7, "to_port": "cin__3"}],
                module="four",
                name="two#1",
            ),
        ],
        "module": CompressedNode("four"),
    },
    {
        "elements": [
            CompressedNode(
                class_name="four",
                node_id=11,
                links=[],
                module="eight",
                name="four#0",
            ),
            CompressedNode(
                class_name="four",
                node_id=12,
                links=[{"from_port": "cout__4__8", "to_id": 11, "to_port": "cin__7"}],
                module="eight",
                name="four#1",
            ),
            CompressedNode(
                class_name="two",
                node_id=8,
                links=[{"from_port": "cout__4", "to_id": 7, "to_port": "cin__3"}],
                module="four",
                name="two#1",
            ),
            CompressedNode(
                class_name="fulladder",
                node_id=4,
                links=[],
                module="two",
                name="fulladder#0",
            ),
        ],
        "module": CompressedNode("eight"),
    },
]


tree_obj = CompressedTree(example_comp)
tree_obj.chain()
tree_obj.decompress()
pprint(tree_obj.tree)

# print(tree_obj.get_leaves())
