#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .componentnode import ComponentNode


class ComponentTree:
    def __init__(self, composition: dict = None, root_key: str = "Home") -> None:

        self.__composition = composition
        self.root_key = root_key
        if self.__composition:
            for module in self.__composition.keys():
                if module == self.root_key:
                    self.__root = module
                    break
        else:
            self.__composition = {}
            self.__root = None

        self.__node_delim = "#"

        self.__leaves = []  # <list(ComponentNode)>
        self.__tree = {}  # <dict(ComponentNode: list(ComponentNode))>
        self.__height = 0

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

        module_node = self.find_module_in_composition(module_name)

        # append a new ComponentNode object with ComponentNode.class_name
        self.__composition[module_node].append(ComponentNode(class_name=element_name))
        current_node = self.__composition[module_node][element_ix]

        current_node.set_module(module_name)
        element_count = self.__get_element_count(element_name)
        current_node.set_name(self.__get_element_name(element_name, element_count))
        current_node.set_type(element_id)
        current_node.set_links(element_links)

    def __get_element_name(self, element_name: str, count: int) -> str:

        return f"{element_name}{self.__node_delim}{count}"

    def __get_element_count(self, element_name: str) -> int:

        count = -1
        for module in self.__composition.keys():
            count += self.__composition[module].count(element_name)

        return count

    def find_module_in_composition(self, element_name: str):

        for module in self.__composition.keys():
            if module == element_name:
                return module

    def __get_elements_from_module(self, node: ComponentNode) -> list:

        for module in self.__composition:
            if module == node:
                return [
                    ComponentNode(
                        class_name=i.class_name,
                        type=i.type,
                        name=i.name,
                        links=i.links,
                        module=i.module,
                    )
                    for i in self.__composition[module]
                ]

        return []

    def __decompress(self, node: ComponentNode) -> dict:
        return {
            node: [self.__decompress(n) for n in self.__get_elements_from_module(node)]
        }

    def decompress(self) -> dict:

        self.__root = self.find_module_in_composition(self.root_key)
        self.__tree = self.__decompress(self.__root)

    def __get_leaves(self, subtree: dict, depth: int = 0) -> None:

        for key, value in subtree.items():
            if not value:
                self.__leaves.append(key)
                self.__height = max(self.__height, depth)

            for node in value:
                self.__get_leaves(node, depth + 1)

    def get_leaves(self) -> list:

        self.__get_leaves(self.__tree)
        return self.__leaves

    def get_height(self) -> int:

        return self.__height

    def get_tree(self) -> dict:

        return self.__tree

