#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from .componenttree import ComponentTree


class CompositionParser:
    def __init__(self, data: dict) -> None:

        self.__raw_data = data
        self.ctree = ComponentTree()

    def __copy_connections(self, element: dict, element_list: dict) -> None:

        output_names = element["data"]["links"]["outputs"]
        output_conns = element["outputs"].values()
        links = []
        for output_name, output_conn in zip(output_names, output_conns):
            for conn in output_conn["connections"]:
                to_node_type = conn["node"]
                to_node_conn_name = conn["output"]
                to_node_conn_num = int(to_node_conn_name[-1]) - 1
                to_node_port = element_list[to_node_type]["data"]["links"]["inputs"][
                    to_node_conn_num
                ]

                links.append(
                    {
                        "from_port": output_name,
                        "to_node_type": int(to_node_type),
                        "to_port": to_node_port,
                    }
                )

        return links

    def filter(self) -> None:

        for module_name, module in self.__raw_data.items():

            self.ctree.add_parent(module_name)

            for component_list in module.values():

                for component_index, component in enumerate(component_list.values()):

                    # append a new CompressedNode object with CompressedNode.class_name
                    self.ctree.add_child(
                        module_name,
                        component["name"],
                        component_index,
                        component["id"],
                        self.__copy_connections(component, component_list),
                    )

    def generate_tree(self) -> ComponentTree:

        self.ctree.decompress()
        return self.ctree

    def dump_raw_data(self, file_name="dump.json"):

        with open(file_name, "w") as dump_file:
            json.dump(self.__raw_data, dump_file, indent=4)
