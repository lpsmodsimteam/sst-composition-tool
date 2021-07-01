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
        "link": {
            "input": [
                # adder-subtractor ports
                "as_sum_0",
                "as_sum_1",
                "as_sum_2",
                "as_sum_3",
                "as_cout_3",
            ],
            "output": [
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
        "link": {
            "input": [
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
            "output": [
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
        "link": {
            "input": [
                "opand1",
                "opand2",
                "cin",
            ],
            "output": ["sum", "cout"],
        },
    },
    {
        "name": "bintodec",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "link": {
            "input": [
                "sum_0",
                "sum_1",
                "sum_2",
                "sum_3",
            ],
            "output": [],
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
            DF_BOX_DIVS[element_name]["link"] = element["link"]
            node_styles += "\n".join(
                NODE_INPUT_STYLE_TEMPL.format(class_name=element_name, index=i + 1, value=j)
                for i, j in enumerate(element["link"]["input"])
            )
            node_styles += "\n".join(
                NODE_OUTPUT_STYLE_TEMPL.format(class_name=element_name, index=i + 1, value=j)
                for i, j in enumerate(element["link"]["output"])
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
        # with open("out.json", "w") as dump_file:
        #     json.dump(data, dump_file, indent=4)
        pprint(data)
        return ""

    return app
