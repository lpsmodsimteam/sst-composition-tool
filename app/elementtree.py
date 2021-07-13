#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint

from .compressedtree import CompressedNode, CompressedTree


class ElementTree(object):
    def __init__(self, data) -> None:

        self.raw_data = data
        self.compositions = {}

        self.node_delim = "#"
        self.module_delim = "%"

    def __get_element_count(self, module_node, element_name) -> int:

        return self.compositions[module_node].count(element_name) - 1

    def __get_element_name(self, element_name, count) -> str:

        return element_name + self.node_delim + str(count)

    def __copy_connections(self, module_node, element, num_module, num_element) -> None:

        output_names = element["data"]["links"]["outputs"]
        output_conns = element["outputs"].values()
        for output_name, output_conn in zip(output_names, output_conns):
            for conn in output_conn["connections"]:
                self.compositions[module_node][num_element].links.append(
                    {
                        "from_port": output_name,
                        "to_id": int(conn["node"]),
                        "to_port": element["data"]["links"]["inputs"][
                            int(conn["output"][-1]) - 1
                        ],
                    }
                )

    def filter(self) -> None:

        num_modules = 0
        for module_name, module in self.raw_data.items():

            # make a new key of type <CompressedNode: list>
            module_node = CompressedNode(class_name=module_name, name=module_name)
            self.compositions[module_node] = []

            for element_list in module.values():

                for num_elements, element in enumerate(element_list.values()):

                    # append a new CompressedNode object with CompressedNode.class_name
                    self.compositions[module_node].append(
                        CompressedNode(class_name=element["name"])
                    )

                    # assign CompressedNode.module_name
                    self.compositions[module_node][num_elements].set_module(module_name)

                    # assign CompressedNode.name
                    element_count = self.__get_element_count(
                        module_node, element["name"]
                    )
                    self.compositions[module_node][num_elements].set_name(
                        self.__get_element_name(element["name"], element_count)
                    )

                    # assign CompressedNode.node_id
                    self.compositions[module_node][num_elements].set_node_id(
                        element["id"]
                    )

                    # assign CompressedNode.links
                    self.compositions[module_node][num_elements].set_links([])
                    self.__copy_connections(
                        module_node, element, num_modules, num_elements
                    )

                num_modules += 1

    def generate_tree(self):

        pprint(self.compositions)
        ctree = CompressedTree(self.compositions)
        ctree.decompress()
        pprint(ctree.tree)

    def dump_raw_data(self):

        with open("out.json", "w") as dump_file:
            json.dump(self.raw_data, dump_file, indent=4)

    @staticmethod
    def __get_name_by_id(links_list, node_id) -> str:

        for i in links_list:
            if i["id"] == node_id:
                return i["name"]

    def convert_to_config(self):

        for element in self.processed_data:
            # print(element)
            for link in element["links"]:
                print(
                    f"""sst.Link('{link["from_port"]}_{element["id"]}').connect(
            ({element["name"]}, "{link["from_port"]}", LINK_DELAY),
            ({self.__get_name_by_id(self.processed_data, link["to_id"])}, "{link["to_port"]}", LINK_DELAY)
        )"""
                )

        pprint(self.processed_data)
