#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint


class ComponentNode:
    def __init__(
        self,
        class_name=None,
        node_id=0,
        name=None,
        links=None,
        module=None,
    ) -> None:

        self.class_name = class_name
        self.name = name
        self.node_id = node_id
        self.links = links
        self.module = module

    def set_class_name(self, class_name: str) -> None:
        self.class_name = class_name

    def set_node_id(self, node_id: int) -> None:
        self.node_id = node_id

    def set_links(self, links: list) -> None:
        self.links = links

    def set_module(self, module: str) -> None:
        self.module = module

    def set_name(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        rep = ""
        if self.links:
            rep = f""" | {self.links[0]["from_port"]}/{self.links[0]["to_id"]}/{self.links[0]["to_port"]}"""
        return f"{self.class_name} ({self.node_id})" + rep

    def __eq__(self, other) -> bool:

        if isinstance(other, ComponentNode):
            return self.class_name == other.class_name

        elif isinstance(other, str):
            return self.class_name == other

        elif isinstance(other, int):
            return self.id == other

    def __hash__(self) -> int:
        return hash(self.class_name)


class ComponentTree:
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
        for k in self.composition.keys():
            if k == self.root_key:
                self.root = k
                break

        self.__leaves = []  # <list(ComponentNode)>
        self.__tree = {}  # <dict(ComponentNode: list(ComponentNode))>

    def __get_children(self, node: ComponentNode) -> list:

        for parent in self.composition:
            if parent == node:
                return [
                    ComponentNode(
                        class_name=i.class_name,
                        node_id=i.node_id,
                        name=i.name,
                        links=i.links,
                        module=i.module,
                    )
                    for i in self.composition[parent]
                ]

        return []

    def __decompress(self, node: ComponentNode) -> dict:
        return {node: [self.__decompress(n) for n in self.__get_children(node)]}

    def decompress(self) -> dict:
        self.__tree = self.__decompress(self.root)

    def get_tree(self) -> dict:

        return self.__tree

    def __get_leaves(self, subtree: ComponentNode) -> None:
        for key, value in subtree.items():
            if not value:
                self.__leaves.append(key)

            for node in value:
                self.__get_leaves(node)

    def get_leaves(self) -> list:

        self.__get_leaves(self.__tree)
        return self.__leaves


if __name__ == "__main__":

    example_comp = {
        ComponentNode(class_name="Home", name="Home"): [
            ComponentNode(
                class_name="eight",
                node_id=13,
                links=[],
                module="Home",
                name="eight#0",
            )
        ],
        ComponentNode(class_name="two"): [
            ComponentNode(
                class_name="fulladder",
                node_id=3,
                links=[],
                module="two",
                name="fulladder#0",
            ),
            ComponentNode(
                class_name="fulladder",
                node_id=4,
                links=[],
                module="two",
                name="fulladder#1",
            ),
        ],
        ComponentNode(class_name="four"): [
            ComponentNode(
                class_name="two", node_id=7, links=[], module="four", name="two#0"
            ),
            ComponentNode(
                class_name="two",
                node_id=8,
                links=[{"from_port": "cout__4", "to_id": 7, "to_port": "cin__3"}],
                module="four",
                name="two#1",
            ),
        ],
        ComponentNode(class_name="eight"): [
            ComponentNode(
                class_name="four",
                node_id=11,
                links=[],
                module="eight",
                name="four#0",
            ),
            ComponentNode(
                class_name="four",
                node_id=12,
                links=[{"from_port": "cout__4__8", "to_id": 11, "to_port": "cin__7"}],
                module="eight",
                name="four#1",
            ),
            ComponentNode(
                class_name="two",
                node_id=8,
                links=[{"from_port": "cout__4", "to_id": 7, "to_port": "cin__3"}],
                module="four",
                name="two#1",
            ),
            ComponentNode(
                class_name="fulladder",
                node_id=4,
                links=[],
                module="two",
                name="fulladder#0",
            ),
        ],
    }

    tree_obj = ComponentTree(example_comp)
    tree_obj.decompress()
    pprint(tree_obj.get_tree(), indent=2)
    pprint(tree_obj.get_leaves(), indent=2)
