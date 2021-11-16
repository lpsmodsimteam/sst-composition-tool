#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from .componenttree import ComponentTree
from .hierarchyresolver import HierarchyResolver
from .boilerplate.sst import (
    COMPONENT_INIT_TEMPL,
    COMPONENT_LINK_TEMPL,
    COMPONENT_PARAM_TEMPL,
)


class CompositionParser:
    def __init__(self, data: dict, library: str) -> None:

        self.__raw_data = data
        self.library = library
        self.ctree = ComponentTree()
        self.resolved_links = []
        self.components_str_list = []
        self.links_str_list = []

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
                        str(component["data"]["param"]),
                    )

    def generate_tree(self) -> ComponentTree:

        self.ctree.decompress()
        return self.ctree

    def dump_raw_data(self, file_name="dump.json") -> None:

        with open(file_name, "w") as dump_file:
            json.dump(self.__raw_data, dump_file, indent=4)

    def resolve_hierarchy(self) -> None:

        hr = HierarchyResolver(self.ctree.get_tree())
        hr.resolve_hierarchy()
        self.resolved_links = hr.get_links()

    def get_resolved_links(self) -> list:

        return self.resolved_links

    def dump_config(self, config_templ_path, config_file_name="run.py"):

        with open(config_templ_path) as config_templ_file:
            config_templ_str = config_templ_file.read()

        with open(config_file_name, "w") as config_file:
            config_file.write(
                config_templ_str.format(
                    init="\n".join(self.components_str_list),
                    links="\n".join(self.links_str_list),
                )
            )

    def generate_config(self) -> None:

        leaves = self.ctree.get_leaves()
        for leaf in leaves:
            self.components_str_list.append(
                COMPONENT_INIT_TEMPL.format(
                    name=leaf, library=self.library, class_name=leaf.class_name
                )
            )
            self.components_str_list.append(
                COMPONENT_PARAM_TEMPL.format(name=leaf, params=leaf.params)
            )

        self.resolved_links = sorted(self.resolved_links, key=lambda x: x[0].id)
        for link in self.resolved_links:
            comp1, link1, comp2, link2 = link
            self.links_str_list.append(
                COMPONENT_LINK_TEMPL.format(
                    comp1=comp1, link1=link1, comp2=comp2, link2=link2
                )
            )
