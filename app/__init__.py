#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pprint import pprint
from pathlib import Path

from flask import Flask, render_template, request

from .templates import (
    DF_BOX_DIVS_TEMPL,
    INPUT_TAG_TEMPL,
    ELEMENT_DIV_TEMPL,
    DF_BOX_DIVS,
    NODE_INPUT_STYLE_TEMPL,
    NODE_OUTPUT_STYLE_TEMPL,
    EXAMPLE_COMPONENTS,
)
from .compositionparser import CompositionParser


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.static_folder = "static"

    @app.route("/")
    def index():

        return render_template("index.html")

    @app.route("/upload")
    def upload():

        element_divs = ""
        node_styles = ""

        for element in EXAMPLE_COMPONENTS:
            input_tags = ""
            element_name = element["name"]

            for param in element["param"].keys():
                input_tags += INPUT_TAG_TEMPL.format(key=param)
            DF_BOX_DIVS[element_name] = {}
            DF_BOX_DIVS[element_name]["html"] = DF_BOX_DIVS_TEMPL.format(
                element=element_name, desc=element["desc"], input_tag=input_tags
            )
            DF_BOX_DIVS[element_name]["links"] = element["links"]
            DF_BOX_DIVS[element_name]["param"] = element["param"]
            node_styles += "\n".join(
                NODE_INPUT_STYLE_TEMPL.format(
                    class_name=element_name, index=i + 1, value=j
                )
                for i, j in enumerate(element["links"]["inputs"])
            )
            node_styles += "\n".join(
                NODE_OUTPUT_STYLE_TEMPL.format(
                    class_name=element_name, index=i + 1, value=j
                )
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

        json_data = json.loads(request.form["drawflow_data"])
        data = json_data["data"]
        library = json_data["library"]
        comp_parser = CompositionParser(data, library)
        comp_parser.filter()
        comp_parser.generate_tree()
        comp_parser.resolve_hierarchy()
        comp_parser.get_resolved_links()
        comp_parser.generate_config()
        comp_parser.dump_config(
            Path(app.static_folder).resolve() / "templates" / "run.templ"
        )

        return ""

    return app
