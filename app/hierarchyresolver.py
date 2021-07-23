from pprint import pprint
from typing import Tuple

from .componentnode import ComponentNode


class HierarchyResolver:
    def __init__(self, component_tree: dict) -> None:
        self.__tree = component_tree
        self.__hierarchy_links = []
        self.__node_delim = "#"

    def __find_element_by_types(self, subtree: dict, type: int) -> ComponentNode:

        for key, value in subtree.items():
            if key.type == type:
                return key, subtree

            for node in value:
                found = self.__find_element_by_types(node, type)
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

    def resolve_connection(self, connection: str) -> Tuple[ComponentNode, str]:

        connection_name, node_types = self.parse_connection(connection)
        subtree = self.__tree

        if not node_types:
            return 0, connection

        while node_types:
            # print("$$$$$", node_types, subtree)
            node, subtree = self.__find_element_by_types(subtree, node_types.pop())
            if not subtree[node]:
                # print(node, connection_name)
                return node, connection_name

    def parse_connection(self, connection: str) -> Tuple[str, ComponentNode]:

        if isinstance(connection, int):
            return "", [connection]

        connection_list = connection.split(self.__node_delim)
        # print(connection_list[0], [int(i) for i in connection_list[1:]])
        return connection_list[0], [int(i) for i in connection_list[1:]]

    def resolve_hierarchy(self, subtree=None):

        # pprint(self.__siblings)
        if not subtree:
            subtree = self.__tree

        # root_module = self.__tree[self.__root]
        for key, value in subtree.items():
            if not value:
                return
            for node in value:
                for k in node.keys():
                    for link in k.links:
                        # print(link)
                        from_element, from_port = self.resolve_connection(
                            link["from_port"]
                        )
                        if not from_element:
                            print(k, self.get_module_from_element(k))
                            from_element = str(k) + "LOLOOL"
                        # print(from_element, from_port)
                        to_element = self.resolve_connection(link["to_id"])
                        if to_element:
                            to_element = to_element[0]
                        to_port = link["to_port"]
                        print(((from_element, from_port), (to_element, to_port)))
                        self.__hierarchy_links.append(
                            ((from_element, from_port), (to_element, to_port))
                        )
                        # pprint(self.__hierarchy_links)
                self.resolve_hierarchy(node)

    def get_hierarchy(self):

        pprint(self.__hierarchy_links)
        # pprint(self.__siblings)
