import json

from flask import Flask, render_template, request


ELEMENTS = [
    {"name": "add", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1, "b": 2}},
    {"name": "sub", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1, "b": 2}},
    {"name": "mul", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1, "b": 2}},
    {"name": "div", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1, "b": 2}},
    {"name": "reg", "param": {"clock": "1MHz", "link_speed": "1ps", "a": 1}},
]

DIV_STR = """<div>
    <div class="title-box"><i class="fas fa-code"></i> {element}</div>
    <div class="box">
        {input_tag}
    </div>
</div>
"""

INPUT_TAG_TEMPL = """<input type="text" df-{key} placeholder="{key}">"""

ELEMENT_DIV_TEMPL = """<div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="{0}">
    <i class="fas fa-code"></i><span> {0}</span>
</div>
"""


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
            df_box_divs[element["name"]] = DIV_STR.format(
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
