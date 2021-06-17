#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template, request

from .templates import DF_BOX_DIVS_TEMPL, INPUT_TAG_TEMPL, ELEMENT_DIV_TEMPL

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

        df_box_divs = {}
        element_divs = ""

        for element in ELEMENTS:
            input_tags = ""
            for k, v in element["param"].items():
                input_tags += INPUT_TAG_TEMPL.format(key=k)
            df_box_divs[element["name"]] = DF_BOX_DIVS_TEMPL.format(
                element=element["name"], input_tag=input_tags
            )
            element_divs += ELEMENT_DIV_TEMPL.format(element["name"])

        return render_template(
            "index.html", element_divs=element_divs, df_box_divs=json.dumps(df_box_divs)
        )

    @app.route("/export_drawflow_data", methods=["POST"])
    def export_data():

        print(json.loads(request.form["drawflow_data"]))
        return ""

    return app
