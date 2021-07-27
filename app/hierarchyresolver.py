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

    def __find_node_by_type(self, subtree: dict, type: int) -> ComponentNode:

        for key, value in subtree.items():
            if key.type == type:
                return key, subtree

            for node in value:
                found = self.__find_node_by_type(node, type)
                if found:
                    return found

    def __find_node_by_id(self, subtree: dict, id: int) -> ComponentNode:

        for key, value in subtree.items():
            if key.id == id:
                return key, subtree

            for node in value:
                found = self.__find_node_by_id(node, id)
                if found:
                    return found

    def get_path_to_root(self, node, node_types_list=None):

        if not node_types_list:
            node_types_list = []

        node_types_list.append(node.type)

        parent = self.get_parent(node)
        node_types_list.append(parent.type)

        while parent.type:
            parent = self.get_parent(parent)
            node_types_list.append(parent.type)

        return node_types_list

    def get_parent(self, node: ComponentNode, subtree=None):

        if not subtree:
            subtree = self.__tree

        for key, value in subtree.items():
            for k in value:
                for l in k.keys():

                    if node.id == l.id:
                        return key

                    parent = self.get_parent(node, k)
                    if parent:
                        return parent

    def resolve_from_port(
        self, node: ComponentNode, connection: str
    ) -> Tuple[ComponentNode, str]:

        connection_name, node_types_list = self.parse_connection(connection)

        if not node_types_list:
            return None, connection

        node_types_list = self.get_path_to_root(node, node_types_list)
        print(node_types_list)

        subtree = self.__tree
        while node_types_list:
            node, subtree = self.__find_node_by_type(subtree, node_types_list.pop())
            if not subtree[node]:
                return node, connection_name

    def resolve_to_port(
        self, node: ComponentNode, to_node_type: int, connection: str
    ) -> Tuple[ComponentNode, str]:

        current_node, _ = self.__find_node_by_id(self.__tree, node.id)
        current_parent = self.get_parent(current_node)
        current_parent, subtree = self.__find_node_by_id(self.__tree, current_parent.id)
        sibling_node = self.__find_node_by_type(subtree, to_node_type)
        if sibling_node:
            sibling_node, subtree = sibling_node
        while not sibling_node:
            current_parent = self.get_parent(current_parent)
            current_parent, subtree = self.__find_node_by_id(
                self.__tree, current_parent.id
            )
            sibling_node = self.__find_node_by_type(subtree, to_node_type)
            if sibling_node:
                sibling_node, subtree = sibling_node

        connection_name, node_types_list = self.parse_connection(connection)

        while node_types_list:
            node, subtree = self.__find_node_by_type(subtree, node_types_list.pop())
            if not subtree[node]:
                return node, connection_name
        else:
            return (
                self.__find_node_by_type(subtree, to_node_type)[0],
                connection_name,
            )

    def parse_connection(self, connection) -> Tuple[str, list]:
        """Parse connection string representing SST Links

        The connection string is split on the node delimter. The first node of the
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

                        from_node, from_port = self.resolve_from_port(
                            k, link["from_port"]
                        )
                        if not from_node:
                            from_node = k
                        to_node, to_port = self.resolve_to_port(
                            k,
                            link["to_node_type"],
                            link["to_port"],
                        )

                        self.__hierarchy_links.append(
                            ((from_node, from_port), (to_node, to_port))
                        )
                self.__resolve_hierarchy(node)

    def get_hierarchy(self):

        pprint(self.__hierarchy_links)
        new_set = set(i[0] for i in self.__hierarchy_links)
        new_set2 = set(i[1] for i in self.__hierarchy_links)
        print(len(self.__hierarchy_links), len(new_set), len(new_set2))
