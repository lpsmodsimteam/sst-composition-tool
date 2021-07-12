#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint


class CompressedNode:
    def __init__(
        self,
        class_name=None,
        name=None,
        node_id=0,
        links=None,
        module=None,
    ) -> None:

        self.class_name = class_name
        self.name = name
        self.node_id = node_id
        self.links = links
        self.module = module

    def set_class_name(self, class_name):
        self.class_name = class_name

    def set_node_id(self, node_id):
        self.node_id = node_id

    def set_links(self, links):
        self.links = links

    def set_module(self, module):
        self.module = module

    def set_name(self, name):
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name} ({id(self)})"

    def __eq__(self, other) -> bool:
        if isinstance(other, CompressedNode):
            return self.class_name == other.class_name

    def __hash__(self) -> int:
        return hash(self.class_name)


class CompressedTree:
    def __init__(
        self,
        composition,
        parent_key="module",
        children_key="elements",
        root_key="Home",
    ) -> None:

        self.composition = composition
        self.parent_key = parent_key
        self.children_key = children_key
        self.root_key = root_key
        for k in self.composition:
            if k[self.parent_key].class_name == self.root_key:
                self.root = k[self.parent_key]

        self.leaves = []
        self.tree = {}

    def __chain(self) -> None:

        self.composition = {
            e[self.parent_key]: e[self.children_key] for e in self.composition
        }

    def __get_children(self, node) -> list:

        for parent in self.composition:
            if parent == node:
                return [
                    CompressedNode(
                        class_name=i.class_name,
                        name=i.name,
                        node_id=i.node_id,
                        links=i.links,
                        module=i.module,
                    )
                    for i in self.composition[parent]
                ]

        return []

    def __decompress(self, node) -> dict:
        return {node: [self.__decompress(n) for n in self.__get_children(node)]}

    def decompress(self) -> dict:
        self.__chain()
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


if __name__ == "__main__":

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
                    links=[
                        {"from_port": "cout__4__8", "to_id": 11, "to_port": "cin__7"}
                    ],
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
    tree_obj.decompress()
    pprint(tree_obj.tree)
