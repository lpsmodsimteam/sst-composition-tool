#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template, request

from .templates import (
    DF_BOX_DIVS_TEMPL,
    INPUT_TAG_TEMPL,
    ELEMENT_DIV_TEMPL,
    HIDDEN_ELEMENT_DIV_TEMPL,
    DF_BOX_DIVS,
)

ELEMENTS = [
    {"name": "add", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1, "b": 2}},
    {"name": "sub", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1, "b": 2}},
    {"name": "mul", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1, "b": 2}},
    {"name": "div", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1, "b": 2}},
    {"name": "reg", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1}},
]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.static_folder = "static"

    @app.route("/")
    def index():

        element_divs = HIDDEN_ELEMENT_DIV_TEMPL

        for element in ELEMENTS:
            input_tags = ""
            element_name = element["name"]

            for k, v in element["param"].items():
                input_tags += INPUT_TAG_TEMPL.format(key=k)
            DF_BOX_DIVS[element_name] = DF_BOX_DIVS_TEMPL.format(
                element=element_name, input_tag=input_tags
            )

            element_divs += ELEMENT_DIV_TEMPL.format(element_name)

        return render_template(
            "index.html", element_divs=element_divs, df_box_divs=json.dumps(DF_BOX_DIVS)
        )

    @app.route("/export_drawflow_data", methods=["POST"])
    def export_data():

        from pprint import pprint

        data = json.loads(request.form["drawflow_data"])["drawflow"]
        pprint(data)
        return ""

    return app
