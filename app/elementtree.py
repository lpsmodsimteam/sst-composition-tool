#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint

from .compressedtree import CompressedNode, CompressedTree


class ElementTree(object):
    def __init__(self, data) -> None:

        self.raw_data = data
        self.processed_data = []
        self.compositions = []

        self.num_elements = 0

        self.node_delim = "#"
        self.module_delim = "%"

    def __get_element_count(self, element_name) -> str:

        count = -1
        for module in self.compositions:
            for element in module["elements"]:
                if element_name == element.class_name:
                    count += 1

        return count

    def __get_element_name(self, element_name, count) -> str:

        return element_name + self.node_delim + str(count)

    @staticmethod
    def __get_name_by_id(links_list, node_id) -> str:

        for i in links_list:
            if i["id"] == node_id:
                return i["name"]

    def __copy_connections(self, element, num_module, num_element) -> None:

        output_names = element["data"]["links"]["outputs"]
        output_conns = element["outputs"].values()
        for output_name, output_conn in zip(output_names, output_conns):
            for conn in output_conn["connections"]:
                self.compositions[num_module]["elements"][num_element].links.append(
                    {
                        "from_port": output_name,
                        "to_id": int(conn["node"]),
                        "to_port": element["data"]["links"]["inputs"][
                            int(conn["output"][-1]) - 1
                        ],
                    }
                )

    def flatten(self) -> None:

        num_modules = 0
        for module_name, module in self.raw_data.items():

            self.compositions.append(
                {"module": CompressedNode(class_name=module_name, name=module_name)}
            )
            self.compositions[num_modules]["elements"] = []
            elements_ptr = self.compositions[num_modules]["elements"]

            for element_list in module.values():

                for num_elements, element in enumerate(element_list.values()):

                    elements_ptr.append(CompressedNode(class_name=element["name"]))

                    elements_ptr[num_elements].set_module(module_name)

                    element_count = self.__get_element_count(element["name"])
                    elements_ptr[num_elements].set_name(
                        self.__get_element_name(element["name"], element_count)
                    )

                    elements_ptr[num_elements].set_node_id(element["id"])

                    elements_ptr[num_elements].set_links([])

                    self.__copy_connections(element, num_modules, num_elements)

                num_modules += 1

    def generate_tree(self):

        pprint(self.compositions)
        ctree = CompressedTree(self.compositions)
        ctree.decompress()
        pprint(ctree.tree)

    # def unroll_modules(self) -> None:

    #     # pprint(self.processed_data)

    #     unrolled_data = []
    #     mod_ctr = 0
    #     max_depth = 1

    #     for module in self.compositions:
    #         for element in module["elements"]:
    #             for module_again in self.compositions:
    #                 if element == module_again["module"]:
    #                     print(module_again["module"], "is a module")

    #                     for link_data in self.processed_data:
    #                         if link_data["module"] == module_again["module"]:
    #                             link_data_copy = link_data.copy()
    #                             link_data_copy["name"] = (
    #                                 link_data_copy["name"]
    #                                 + self.module_delim
    #                                 + module_again["module"]
    #                                 + self.node_delim
    #                                 + str(mod_ctr)
    #                             )
    #                             unrolled_data.append(link_data_copy)
    #                     mod_ctr += 1

    #     pprint(unrolled_data)

    def dump_raw_data(self):

        with open("out.json", "w") as dump_file:
            json.dump(self.raw_data, dump_file, indent=4)

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
