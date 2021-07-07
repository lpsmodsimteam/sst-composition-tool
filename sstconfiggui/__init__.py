#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template, request

from .templates import (
    DF_BOX_DIVS_TEMPL,
    INPUT_TAG_TEMPL,
    ELEMENT_DIV_TEMPL,
    DF_BOX_DIVS,
    NODE_INPUT_STYLE_TEMPL,
    NODE_OUTPUT_STYLE_TEMPL,
)

ELEMENTS = [
    {
        "name": "addsub",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
            "control": 0,
            "opand1": [1, 1, 0, 1],
            "opand2": [0, 1, 0, 1],
        },
        "links": {
            "inputs": [
                # adder-subtractor ports
                "as_sum_0",
                "as_sum_1",
                "as_sum_2",
                "as_sum_3",
                "as_cout_3",
            ],
            "outputs": [
                # adder-subtractor ports
                "as_opand1_0",
                "as_opand1_1",
                "as_opand1_2",
                "as_opand1_3",
                "as_opand2_0",
                "as_opand2_1",
                "as_opand2_2",
                "as_opand2_3",
                # bintodec ports
                "b2d_sum_0",
                "b2d_sum_1",
                "b2d_sum_2",
                "b2d_sum_3",
                "b2d_cout_3",
            ],
        },
    },
    {
        "name": "ripplecarryadder",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                # full adder ports
                "as_opand1_0",
                "as_opand1_1",
                "as_opand1_2",
                "as_opand1_3",
                "as_opand2_0",
                "as_opand2_1",
                "as_opand2_2",
                "as_opand2_3",
                "as_cin_0",
                # adder-subtractor ports
                "add_sum_0",
                "add_sum_1",
                "add_sum_2",
                "add_sum_3",
                "add_cout_0",
                "add_cout_1",
                "add_cout_2",
                "add_cout_3",
            ],
            "outputs": [
                # full adder ports
                "add_opand1_0",
                "add_opand1_1",
                "add_opand1_2",
                "add_opand1_3",
                "add_opand2_0",
                "add_opand2_1",
                "add_opand2_2",
                "add_opand2_3",
                "add_cin_0",
                "add_cin_1",
                "add_cin_2",
                "add_cin_3",
                # adder-subtractor ports
                "as_sum_0",
                "as_sum_1",
                "as_sum_2",
                "as_sum_3",
                "as_cout_3",
            ],
        },
    },
    {
        "name": "fulladder",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "opand1",
                "opand2",
                "cin",
            ],
            "outputs": ["sum", "cout"],
        },
    },
    {
        "name": "bintodec",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "sum_0",
                "sum_1",
                "sum_2",
                "sum_3",
            ],
            "outputs": [],
        },
    },
]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.static_folder = "static"

    @app.route("/")
    def index():

        element_divs = ""
        node_styles = ""

        for element in ELEMENTS:
            input_tags = ""
            element_name = element["name"]

            for param in element["param"].keys():
                input_tags += INPUT_TAG_TEMPL.format(key=param)
            DF_BOX_DIVS[element_name] = {}
            DF_BOX_DIVS[element_name]["html"] = DF_BOX_DIVS_TEMPL.format(
                element=element_name, input_tag=input_tags
            )
            DF_BOX_DIVS[element_name]["links"] = element["links"]
            DF_BOX_DIVS[element_name]["param"] = element["param"]
            node_styles += "\n".join(
                NODE_INPUT_STYLE_TEMPL.format(class_name=element_name, index=i + 1, value=j)
                for i, j in enumerate(element["links"]["inputs"])
            )
            node_styles += "\n".join(
                NODE_OUTPUT_STYLE_TEMPL.format(class_name=element_name, index=i + 1, value=j)
                for i, j in enumerate(element["links"]["outputs"])
            )

            element_divs += ELEMENT_DIV_TEMPL.format(element_name)

        return render_template(
            "index.html",
            element_divs=element_divs,
            df_box_divs=json.dumps(DF_BOX_DIVS),
            node_styles=node_styles,
        )

    @app.route("/export_drawflow_data", methods=["POST"])
    def export_data():

        from pprint import pprint

        data = json.loads(request.form["drawflow_data"])["drawflow"]
        new_data = []
        compositions = {}
        connections = []
        with open("out.json", "w") as dump_file:
            json.dump(data, dump_file, indent=4)

        def get_element_count(module, element_name):

            count = 0
            for i in module:
                if i.split("__")[0] == element_name:
                    count += 1

            return element_name + "__" + str(count)

        num_elements = 0
        for module_name, module in data.items():
            compositions[module_name] = []
            for element_list in module.values():
                for i, element in enumerate(element_list.values()):
                    new_data.append({})
                    compositions[module_name].append(
                        get_element_count(compositions[module_name], element["name"])
                    )
                    output_names = element["data"]["links"]["outputs"]
                    output_conns = element["outputs"].values()

                    new_data[num_elements]["module"] = module_name
                    new_data[num_elements]["name"] = compositions[module_name][i]
                    new_data[num_elements]["id"] = element["id"]

                    print((module_name, compositions[module_name][i]))
                    num_elements += 1
                    for output_name, output_conn in zip(output_names, output_conns):
                        for conn in output_conn["connections"]:
                            print((element["id"], conn["node"]))
                            print(
                                (
                                    output_name,
                                    element["data"]["links"]["inputs"][int(conn["output"][-1]) - 1],
                                )
                            )
                            # print(
                            #     input_num,
                            #     (input_name, input_conns),
                            #     conn["node"],
                            #     element_list[conn["node"]]["name"],
                            #     element["data"]["links"]["outputs"][int(conn["input"][-1]) - 1],
                            # )

                #     new_inputs = []
                #     new_outputs = []
                #     for i in ELEMENTS:
                #         if i["name"] == element["name"]:
                #                 print(element["id"], input_num, input_name, input_conns)
                #             for output_num, (output_name, output_conns) in zip(
                #                 i["links"]["outputs"], element["outputs"].items()
                #             ):
                #                 for conn in output_conns["connections"]:
                #                     print(
                #                         (element["id"], conn["node"]),
                #                         element_list[conn["node"]]["name"],
                #                         output_num,
                #                         i["links"]["inputs"][int(conn["outputs"][-1]) - 1],
                #                     )
                #                 print(element["id"], output_num, output_name, output_conns)

                #     new_data.append(
                #         {
                #             "id": element["id"],
                #             "name": element["name"],
                #             "inputs": element["inputs"],
                #             "outputs": element["outputs"],
                #         }
                #     )

        pprint(new_data)
        return ""

    return app
