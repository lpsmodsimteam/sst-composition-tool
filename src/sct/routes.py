import json
from pathlib import Path

from flask import Blueprint, Response, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from .composition import CompositionParser
from .db.checkpoint import Database

bp = Blueprint("bp", __name__)


def valid_checkpoint(file_name: str) -> bool:

    fp = Path(file_name)
    return fp.is_file() and fp.suffix == ".json"


@bp.route("/")
def index() -> str:

    return render_template("index.html")


@bp.route("/canvas")
@bp.route("/canvas/<checkpoint>")
def canvas(checkpoint: str = None) -> str:

    element_divs = ""
    node_styles = ""
    df_box_divs = {}
    imported_drawflow = {}

    if checkpoint and valid_checkpoint(checkpoint):
        with open(checkpoint) as fp:
            checkpoint_data = json.loads(fp.read())
            if "drawflow" in checkpoint_data:
                imported_drawflow = {"drawflow": checkpoint_data["drawflow"]}
                element_divs = checkpoint_data["element_list_html"]
                df_box_divs = checkpoint_data["df_box_divs"]
                node_styles = checkpoint_data["node_styles_html"]

    return render_template(
        "canvas.html",
        element_divs=element_divs,
        df_box_divs=json.dumps(df_box_divs),
        node_styles=node_styles,
        imported_drawflow=imported_drawflow,
    )


@bp.route("/import", methods=["POST"])
def import_checkpoint() -> Response:

    checkpoint = request.files["checkpoint"]
    if valid_checkpoint(checkpoint.filename):
        file_name = secure_filename(checkpoint.filename)
        return redirect(url_for("canvas", checkpoint=file_name))

    return Response(status=500)


@bp.route("/export", methods=["POST"])
def export_checkpoint() -> Response:

    drawflow_data = json.loads(request.form["drawflow_data"])

    db = Database(drawflow_data["library"])
    db.load_history()
    db.save_checkpoint(drawflow_data)

    comp_parser = CompositionParser(drawflow_data["drawflow"], drawflow_data["library"])
    comp_parser.parse()
    comp_parser.generate_config()
    config_templ_str = render_template("run.py", **comp_parser.get_config())
    comp_parser.dump_config("run.py", config_templ_str)

    return Response(status=200)
