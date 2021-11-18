#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Flask, Response, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from .boilerplate.demo import DEMO_COMPONENTS
from .boilerplate.html import (
    DF_BOX_DIVS,
    ELEMENT_DIV,
    INPUT_TAG,
    NODE_INPUT_STYLE,
    NODE_OUTPUT_STYLE,
)
from .compositionparser import CompositionParser


def create_app() -> Flask:
    """
    The Flask application factory function.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.static_folder = "static"
    app.url_map.strict_slashes = False
    app.config["UPLOAD_FOLDER"] = "db"

    @app.route("/")
    def index() -> str:

        return render_template("index.html")

    @app.route("/canvas")
    @app.route("/canvas/<saved_config_file>")
    def canvas(saved_config_file=None) -> str:

        print(saved_config_file)

        return render_template("canvas.html")

    @app.route("/demo")
    def demo() -> str:

        element_divs = ""
        node_styles = ""
        df_box_divs = {}

        for element in DEMO_COMPONENTS:
            input_tags = ""
            element_name = element["name"]

            for param in element["param"].keys():
                input_tags += INPUT_TAG.format(key=param)
            df_box_divs[element_name] = {}
            df_box_divs[element_name]["html"] = DF_BOX_DIVS.format(
                element=element_name, desc=element["desc"], input_tag=input_tags
            )
            df_box_divs[element_name]["links"] = element["links"]
            df_box_divs[element_name]["param"] = element["param"]
            node_styles += "\n".join(
                NODE_INPUT_STYLE.format(class_name=element_name, index=i + 1, value=j)
                for i, j in enumerate(element["links"]["inputs"])
            )
            node_styles += "\n".join(
                NODE_OUTPUT_STYLE.format(class_name=element_name, index=i + 1, value=j)
                for i, j in enumerate(element["links"]["outputs"])
            )

            element_divs += ELEMENT_DIV.format(element_name)

        return render_template(
            "canvas.html",
            element_divs=element_divs,
            df_box_divs=json.dumps(df_box_divs),
            node_styles=node_styles,
        )

    @app.route("/import_data", methods=["POST"])
    def import_data() -> Response:

        saved_config_file = request.files["saved_config_file"]
        if saved_config_file.filename.rsplit(".", 1)[1].lower() == "json":
            file_name = secure_filename(saved_config_file.filename)
            return redirect(url_for("canvas", saved_config_file=file_name))

        return Response(status=500)

    @app.route("/export_drawflow_data", methods=["POST"])
    def export_data() -> Response:

        json_data = json.loads(request.form["drawflow_data"])

        with open("save.json", "w") as fp:
            json.dump(json_data, fp)

        comp_parser = CompositionParser(json_data["drawflow"], json_data["library"])
        comp_parser.parse()
        comp_parser.generate_config()
        config_templ_str = render_template("run.py", **comp_parser.get_config())
        comp_parser.dump_config("run.py", config_templ_str)

        return Response(status=200)

    return app
