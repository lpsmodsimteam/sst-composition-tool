#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from typing import Tuple

from .componentnode import ComponentNode


class HierarchyResolver:
    def __init__(self, component_tree: dict) -> None:
        self.__tree = component_tree
        self.__hierarchy_links = []
        self.__node_delim = "#"

    def __find_element_by_type(self, subtree: dict, type: int) -> ComponentNode:

        for key, value in subtree.items():
            if key.type == type:
                return key, subtree

            for node in value:
                found = self.__find_element_by_type(node, type)
                if found:
                    return found

    def __find_element_by_id(self, subtree: dict, id: int) -> ComponentNode:

        for key, value in subtree.items():
            if key.id == id:
                return key, subtree

            for node in value:
                found = self.__find_element_by_id(node, id)
                if found:
                    return found

    def get_module_from_element(self, element: ComponentNode, subtree=None):

        if not subtree:
            subtree = self.__tree

        for key, value in subtree.items():
            for node in value:
                for l in node.keys():

                    if element.id == l.id:
                        return key

                    found_module = self.get_module_from_element(element, node)
                    if found_module:
                        return found_module

    def resolve_from_port(
        self, node: ComponentNode, connection: str
    ) -> Tuple[ComponentNode, str]:

        connection_name, node_types_list = self.parse_connection(connection)

        if not node_types_list:
            return None, connection

        current_node, _ = self.__find_element_by_id(self.__tree, node.id)
        current_module = self.get_module_from_element(current_node)

        node_types_list.append(node.type)
        node_types_list.append(current_module.type)
        while current_module.type:
            current_module = self.get_module_from_element(current_module)
            node_types_list.append(current_module.type)

        print(node_types_list, node, end=" ")

        subtree = self.__tree
        while node_types_list:
            node, subtree = self.__find_element_by_type(subtree, node_types_list.pop())
            if not subtree[node]:
                print(node, connection_name)
                return node, connection_name

    def resolve_to_port(
        self, node: ComponentNode, to_node_type: int, connection: str
    ) -> Tuple[ComponentNode, str]:

        current_node, _ = self.__find_element_by_id(self.__tree, node.id)
        current_module = self.get_module_from_element(current_node)
        current_module, subtree = self.__find_element_by_id(
            self.__tree, current_module.id
        )
        sibling_node = self.__find_element_by_type(subtree, to_node_type)
        if sibling_node:
            sibling_node, subtree = sibling_node
        while not sibling_node:
            current_module = self.get_module_from_element(current_module)
            current_module, subtree = self.__find_element_by_id(
                self.__tree, current_module.id
            )
            sibling_node = self.__find_element_by_type(subtree, to_node_type)
            if sibling_node:
                sibling_node, subtree = sibling_node

        connection_name, node_types_list = self.parse_connection(connection)

        while node_types_list:
            node, subtree = self.__find_element_by_type(subtree, node_types_list.pop())
            if not subtree[node]:
                return node, connection_name
        else:
            return (
                self.__find_element_by_type(subtree, to_node_type)[0],
                connection_name,
            )

    def parse_connection(self, connection) -> Tuple[str, list]:
        """Parse connection string representing SST Links

        The connection string is split on the node delimter. The first element of the
        list is the name of the connection, and the rest of the list is its nested types
        """
        connection_list = connection.split(self.__node_delim)
        return connection_list[0], [int(i) for i in connection_list[1:]]

    def resolve_hierarchy(self):

        self.__resolve_hierarchy(self.__tree)

    def __resolve_hierarchy(self, subtree):

        for value in subtree.values():
            if not value:
                return
            for node in value:
                for k in node.keys():
                    for link in k.links:

                        from_element, from_port = self.resolve_from_port(
                            k, link["from_port"]
                        )
                        if not from_element:
                            from_element = k
                        to_element, to_port = self.resolve_to_port(
                            k,
                            link["to_node_type"],
                            link["to_port"],
                        )

                        self.__hierarchy_links.append(
                            ((from_element, from_port), (to_element, to_port))
                        )
                self.__resolve_hierarchy(node)

    def get_hierarchy(self):

        pprint(self.__hierarchy_links)
