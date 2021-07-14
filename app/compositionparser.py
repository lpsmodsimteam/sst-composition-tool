#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint

from .componenttree import ComponentNode, ComponentTree


class CompositionParser:
    def __init__(self, data: dict) -> None:

        self.__raw_data = data
        self.__compositions = {}

        self.__node_delim = "#"
        self.__module_delim = "%"

    def __get_element_count(self, module_node: ComponentNode, element_name: str) -> int:

        return self.__compositions[module_node].count(element_name) - 1

    def __get_element_name(self, element_name: str, count: int) -> str:

        return element_name + self.__node_delim + str(count)

    def __copy_connections(self, module_node: ComponentNode, element: dict) -> None:

        output_names = element["data"]["links"]["outputs"]
        output_conns = element["outputs"].values()
        for output_name, output_conn in zip(output_names, output_conns):
            for conn in output_conn["connections"]:
                module_node.links.append(
                    {
                        "from_port": output_name,
                        "to_id": int(conn["node"]),
                        "to_port": element["data"]["links"]["inputs"][
                            int(conn["output"][-1]) - 1
                        ],
                    }
                )

    def filter(self) -> None:

        for module_name, module in self.__raw_data.items():

            # make a new key of type <CompressedNode: list>
            module_node = ComponentNode(class_name=module_name, name=module_name)
            self.__compositions[module_node] = []

            for element_list in module.values():

                for num_elements, element in enumerate(element_list.values()):

                    # append a new CompressedNode object with CompressedNode.class_name
                    self.__compositions[module_node].append(
                        ComponentNode(class_name=element["name"])
                    )
                    current_node = self.__compositions[module_node][num_elements]

                    # assign CompressedNode.module_name
                    current_node.set_module(module_name)

                    # assign CompressedNode.name
                    element_count = self.__get_element_count(
                        module_node, element["name"]
                    )
                    current_node.set_name(
                        self.__get_element_name(element["name"], element_count)
                    )

                    # assign CompressedNode.node_id
                    current_node.set_node_id(element["id"])

                    # assign CompressedNode.links
                    current_node.set_links([])
                    self.__copy_connections(current_node, element)

    def generate_tree(self):

        pprint(self.__compositions)
        ctree = ComponentTree(self.__compositions)
        ctree.decompress()
        pprint(ctree.get_tree())

    def dump_raw_data(self):

        with open("out.json", "w") as dump_file:
            json.dump(self.__raw_data, dump_file, indent=4)

    # @staticmethod
    # def __get_name_by_id(links_list, node_id) -> str:

    #     for i in links_list:
    #         if i["id"] == node_id:
    #             return i["name"]

    # def convert_to_config(self):

    #     for element in self.processed_data:
    #         # print(element)
    #         for link in element["links"]:
    #             print(
    #                 f"""sst.Link('{link["from_port"]}_{element["id"]}').connect(
    #         ({element["name"]}, "{link["from_port"]}", LINK_DELAY),
    #         ({self.__get_name_by_id(self.processed_data, link["to_id"])}, "{link["to_port"]}", LINK_DELAY)
    #     )"""
    #             )

    #     pprint(self.processed_data)
