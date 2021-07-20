#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint


class ComponentNode:
    def __init__(
        self,
        class_name: str = None,
        node_id: int = 0,
        name: str = None,
        links: list = None,
        module: str = None,
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
        # debugging method
        rep = ""
        if self.links:
            rep += " | "
            for link in self.links:
                rep += f"""{link["from_port"]}/{link["to_id"]}/{link["to_port"]}"""
                if len(self.links) > 1:
                    rep += ",\n"
        return f"{self.name} ({self.node_id})" + rep

    def __eq__(self, other) -> bool:

        if isinstance(other, ComponentNode):
            return self.class_name == other.class_name

        elif isinstance(other, str):
            return self.class_name == other

        elif isinstance(other, int):
            return self.node_id == other

    def __hash__(self) -> int:
        return hash(self.class_name)


class ComponentTree:
    def __init__(self, composition: dict = None, root_key: str = "Home") -> None:

        self.__composition = composition
        self.root_key = root_key
        if self.__composition:
            for module in self.__composition.keys():
                if module == self.root_key:
                    self.root = module
                    break
        else:
            self.__composition = {}
            self.root = None

        self.__node_delim = "#"
        self.__module_delim = "%"

        self.__leaves = []  # <list(ComponentNode)>
        self.__tree = {}  # <dict(ComponentNode: list(ComponentNode))>
        self.__max_depth: int = 0

    def __get_element_name(self, element_name: str, count: int) -> str:

        return f"{element_name}{self.__node_delim}{count}"

    def find_module_by_name(self, element_name: str):

        for module in self.__composition.keys():
            if module == element_name:
                return module

    def __get_element_count(self, element_name: str) -> int:

        count = -1
        for module in self.__composition.keys():
            count += self.__composition[module].count(element_name)

        return count

    def add_module(self, module_name: str):

        module_node = ComponentNode(class_name=module_name, name=module_name)
        self.__composition[module_node] = []

    def add_element(
        self,
        module_name: str,
        element_name: str,
        element_ix: int,
        element_id: str,
        element_links: str,
    ):

        module_node = self.find_module_by_name(module_name)

        # append a new CompressedNode object with CompressedNode.class_name
        self.__composition[module_node].append(ComponentNode(class_name=element_name))
        current_node = self.__composition[module_node][element_ix]

        current_node.set_module(module_name)
        element_count = self.__get_element_count(element_name)
        current_node.set_name(self.__get_element_name(element_name, element_count))
        current_node.set_node_id(element_id)
        current_node.set_links(element_links)

    def __get_elements_from_module(self, node: ComponentNode) -> list:

        for parent in self.__composition:
            if parent == node:
                return [
                    ComponentNode(
                        class_name=i.class_name,
                        node_id=i.node_id,
                        name=i.name,
                        links=i.links,
                        module=i.module,
                    )
                    for i in self.__composition[parent]
                ]

        return []

    def __decompress(self, node: ComponentNode) -> dict:
        return {
            node: [self.__decompress(n) for n in self.__get_elements_from_module(node)]
        }

    def __set_root(self):

        if not self.root:
            for module in self.__composition.keys():
                if module == self.root_key:
                    self.root = module
                    break

    def decompress(self) -> dict:

        self.__set_root()
        self.__tree = self.__decompress(self.root)

    def get_tree(self) -> dict:

        return self.__tree

    def __find_element_by_id(
        self, subtree: dict, found_elements: list, node_id: int
    ) -> None:

        for key, value in subtree.items():
            if key.node_id == node_id:
                found_elements.append(key)

            for node in value:
                self.__find_element_by_id(node, found_elements, node_id)

    def find_element_by_id(self, node_id: int) -> list:

        found_elements = []
        self.__find_element_by_id(self.__tree, found_elements, node_id)
        return found_elements

    def __get_leaves(self, subtree: dict, depth: int = 0) -> None:

        for key, value in subtree.items():
            if not value:
                self.__leaves.append(key)
                self.__max_depth = max(self.__max_depth, depth)

            for node in value:
                self.__get_leaves(node, depth + 1)

    def get_leaves(self) -> list:

        self.__get_leaves(self.__tree)
        print("max depth", self.__max_depth)
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
                links=[{"from_port": "cout#4", "to_id": 7, "to_port": "cin#3"}],
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
                links=[{"from_port": "cout#4#8", "to_id": 11, "to_port": "cin#7"}],
                module="eight",
                name="four#1",
            ),
            ComponentNode(
                class_name="two",
                node_id=8,
                links=[{"from_port": "cout#4", "to_id": 7, "to_port": "cin#3"}],
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