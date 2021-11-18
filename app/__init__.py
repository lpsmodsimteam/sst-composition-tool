#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import Flask, Response, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

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
    @app.route("/demo")
    def canvas(saved_config_file=None) -> str:

        element_divs = ""
        node_styles = ""
        df_box_divs = {}
        imported_drawflow = {}

        # ---------- DEMO FUNCTIONALITY ----------
        if request.path == "/demo":

            from . import demo

            (element_divs, df_box_divs, node_styles) = demo.__generate_drawflow(
                element_divs, df_box_divs, node_styles
            )
        # ---------- DEMO FUNCTIONALITY ----------

        elif saved_config_file:
            with open(saved_config_file) as fp:
                saved_config = json.loads(fp.read())
                imported_drawflow = {"drawflow": saved_config["drawflow"]}
                element_divs = saved_config["element_list_html"]
                df_box_divs = saved_config["df_box_divs"]
                node_styles = saved_config["node_styles_html"]

        return render_template(
            "canvas.html",
            element_divs=element_divs,
            df_box_divs=json.dumps(df_box_divs),
            node_styles=node_styles,
            imported_drawflow=imported_drawflow,
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
