import json

from flask import Blueprint, Response, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from .composition import CompositionParser

bp = Blueprint("bp", __name__)


def valid_file_name(file_name: str) -> bool:

    file_name_split = file_name.rsplit(".", 1)
    if len(file_name_split) == 2:
        return file_name_split[1].lower() == "json"

    return False


@bp.route("/")
def index() -> str:

    return render_template("index.html")


@bp.route("/canvas")
@bp.route("/canvas/<saved_config_file>")
def canvas(saved_config_file=None) -> str:

    element_divs = ""
    node_styles = ""
    df_box_divs = {}
    imported_drawflow = {}

    if saved_config_file and valid_file_name(saved_config_file):
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


@bp.route("/import_data", methods=["POST"])
def import_data() -> Response:

    saved_config_file = request.files["saved_config_file"]
    if valid_file_name(saved_config_file.filename):
        file_name = secure_filename(saved_config_file.filename)
        return redirect(url_for("canvas", saved_config_file=file_name))

    return Response(status=500)


@bp.route("/export_drawflow_data", methods=["POST"])
def export_data() -> Response:

    json_data = json.loads(request.form["drawflow_data"])

    with open("save.json", "w") as fp:
        json.dump(json_data, fp)

    comp_parser = CompositionParser(json_data["drawflow"], json_data["library"])
    comp_parser.dump_raw_data()
    comp_parser.parse()
    comp_parser.generate_config()
    config_templ_str = render_template("run.py", **comp_parser.get_config())
    comp_parser.dump_config("run.py", config_templ_str)

    return Response(status=200)
