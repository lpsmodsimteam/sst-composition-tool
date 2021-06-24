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
        "name": "add",
        "param": {"clock": "1MHz", "link_speed": "1ps", "bits": "16"},
        "link": {"input": ["opand_din"], "output": ["sum_dout", "of_dout"]},
    },
    {
        "name": "sub",
        "param": {"clock": "1MHz", "link_speed": "1ps", "bits": "16"},
        "link": {"input": ["opand_din"], "output": ["diff_dout", "neg_dout", "of_dout"]},
    },
    {
        "name": "mul",
        "param": {"clock": "1MHz", "link_speed": "1ps", "bits": "16"},
        "link": {"input": ["opand_din"], "output": ["prod_dout", "of_dout"]},
    },
    {
        "name": "div",
        "param": {"clock": "1MHz", "link_speed": "1ps", "bits": "16"},
        "link": {"input": ["opand_din"], "output": ["div_dout", "of_dout"]},
    },
    {
        "name": "reg",
        "param": {"clock": "1MHz", "link_speed": "1ps", "bits": "16"},
        "link": {"input": ["reg_din"], "output": ["reg_dout", "of_dout"]},
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
            print()
            node_styles += "\n".join(
                [
                    NODE_INPUT_STYLE_TEMPL.format(class_name=element_name, index=i + 1, value=j)
                    for i, j in enumerate(element["link"]["input"])
                ]
            )
            node_styles += "\n".join(
                [
                    NODE_OUTPUT_STYLE_TEMPL.format(class_name=element_name, index=i + 1, value=j)
                    for i, j in enumerate(element["link"]["output"])
                ]
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
        pprint(data)
        return ""

    return app
