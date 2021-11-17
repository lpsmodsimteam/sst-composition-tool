#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from .boilerplate.sst import (
    COMPONENT_INIT_TEMPL,
    COMPONENT_LINK_TEMPL,
    COMPONENT_PARAM_TEMPL,
)
from .componenttree import ComponentTree
from .hierarchyresolver import HierarchyResolver


class CompositionParser:
    def __init__(self, data: dict, library: str) -> None:

        self.__raw_data = data
        self.__library = library
        self.__ctree = ComponentTree()
        self.__components_str_list = []
        self.__links_str_list = []
        self.__resolved_links = []

    def __copy_connections(self, component: dict, component_list: dict) -> None:

        output_names = component["data"]["links"]["outputs"]
        output_conns = component["outputs"].values()
        links = []
        for output_name, output_conn in zip(output_names, output_conns):
            for conn in output_conn["connections"]:
                to_node_type = conn["node"]
                to_node_conn_name = conn["output"]
                to_node_conn_num = int(to_node_conn_name[-1]) - 1
                to_node_port = component_list[to_node_type]["data"]["links"]["inputs"][
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

            self.__ctree.add_parent(module_name)

            for component_list in module.values():

                for component_index, component in enumerate(component_list.values()):

                    # append a new CompressedNode object with CompressedNode.class_name
                    self.__ctree.add_child(
                        module_name,
                        component["name"],
                        component_index,
                        component["id"],
                        self.__copy_connections(component, component_list),
                        str(component["data"]["param"]),
                    )

    def generate_tree(self) -> ComponentTree:

        self.__ctree.decompress()
        return self.__ctree

    def dump_raw_data(self, file_name="dump.json") -> None:

        with open(file_name, "w") as dump_file:
            json.dump(self.__raw_data, dump_file, indent=4)

    def resolve_hierarchy(self) -> None:

        hr = HierarchyResolver(self.__ctree.get_tree())
        hr.resolve_hierarchy()
        self.__resolved_links = hr.get_links()

    def get_resolved_links(self) -> list:

        return self.__resolved_links

    def generate_config(self) -> None:

        leaves = self.__ctree.get_leaves()
        for leaf in leaves:
            self.__components_str_list.append(
                COMPONENT_INIT_TEMPL.format(
                    name=leaf, library=self.__library, class_name=leaf.class_name
                )
            )
            self.__components_str_list.append(
                COMPONENT_PARAM_TEMPL.format(name=leaf, params=leaf.params)
            )

        self.__resolved_links = sorted(self.__resolved_links, key=lambda x: x[0].id)
        for link in self.__resolved_links:
            comp1, link1, comp2, link2 = link
            self.__links_str_list.append(
                COMPONENT_LINK_TEMPL.format(
                    comp1=comp1, link1=link1, comp2=comp2, link2=link2
                )
            )

    def get_config(self) -> dict:

        return {
            "init": "\n".join(self.__components_str_list),
            "links": "\n".join(self.__links_str_list),
        }

    def dump_config(self, config_file_name, config_templ_str):

        with open(config_file_name, "w") as config_file:
            config_file.write(config_templ_str)
