#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint


class GraphDataProcessor(object):
    def __init__(self, data) -> None:

        self.raw_data = data
        self.processed_data = []
        self.compositions = []

        self.num_elements = 0
        self.num_modules = 0

    def __get_element_count(self, element_name):

        count = -1
        for i in self.compositions:
            count += i["elements"].count(element_name)

        return str(count)

    @staticmethod
    def __get_name_by_id(links_list, node_id):

        for i in links_list:
            if i["id"] == node_id:
                return i["name"]

    def flatten(self):

        for module_name, module in self.raw_data.items():

            self.compositions.append({"module": module_name})
            self.compositions[self.num_modules]["elements"] = []

            for element_list in module.values():

                for element in element_list.values():

                    self.compositions[self.num_modules]["elements"].append(element["name"])
                    self.processed_data.append({})

                    self.processed_data[self.num_elements]["module"] = module_name
                    self.processed_data[self.num_elements]["name"] = (
                        element["name"] + "__" + self.__get_element_count(element["name"])
                    )
                    self.processed_data[self.num_elements]["id"] = element["id"]
                    self.processed_data[self.num_elements]["links"] = []

                    output_names = element["data"]["links"]["outputs"]
                    output_conns = element["outputs"].values()

                    for output_name, output_conn in zip(output_names, output_conns):
                        for conn in output_conn["connections"]:
                            self.processed_data[self.num_elements]["links"].append(
                                {
                                    "from_port": output_name,
                                    "to_id": int(conn["node"]),
                                    "to_port": element["data"]["links"]["inputs"][
                                        int(conn["output"][-1]) - 1
                                    ],
                                }
                            )

                    self.num_elements += 1

                self.num_modules += 1

    def unroll_modules(self):

        # pprint(self.processed_data)

        unrolled_data = []
        counter = 0

        for module in self.compositions:
            for element in module["elements"]:
                for module_again in self.compositions:
                    if element == module_again["module"]:
                        print(module_again["module"], "is a module")

                        for link_data in self.processed_data:
                            if link_data["module"] == module_again["module"]:
                                link_data_copy = link_data.copy()
                                link_data_copy["name"] = f"""{link_data_copy["name"]}__{counter}"""
                                unrolled_data.append(link_data_copy)
                        counter += 1

        pprint(unrolled_data)

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
