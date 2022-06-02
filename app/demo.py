import json

from flask import Blueprint, render_template

from .boilerplate.html import (
    DF_BOX_DIVS,
    ELEMENT_DIV,
    INPUT_TAG,
    NODE_INPUT_STYLE,
    NODE_OUTPUT_STYLE,
)


DEMO_COMPONENTS = [
    {
        "name": "addsub",
        "desc": "Description of addsub",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
            "control": 0,
            "opand1": [1, 1, 0, 1],
            "opand2": [0, 1, 0, 1],
        },
        "links": {
            "inputs": [
                # adder-subtractor ports
                "as_sum_0",
                "as_sum_1",
                "as_sum_2",
                "as_sum_3",
                "as_cout_3",
            ],
            "outputs": [
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
        "desc": "Description of ripplecarryadder",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
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
            "outputs": [
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
        "desc": "Description of fulladder",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "opand1",
                "opand2",
                "cin",
            ],
            "outputs": ["sum", "cout"],
        },
    },
    {
        "name": "bintodec",
        "desc": "Description of bintodec",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "sum_0",
                "sum_1",
                "sum_2",
                "sum_3",
            ],
            "outputs": [],
        },
    },
]


def __generate_drawflow(element_divs, df_box_divs, node_styles) -> tuple:

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

    return (
        element_divs,
        df_box_divs,
        node_styles,
    )


demo_bp = Blueprint("demo_bp", __name__)


@demo_bp.route("/demo")
def demo() -> str:

    element_divs = ""
    node_styles = ""
    df_box_divs = {}
    imported_drawflow = {}

    (element_divs, df_box_divs, node_styles) = __generate_drawflow(
        element_divs, df_box_divs, node_styles
    )

    return render_template(
        "canvas.html",
        element_divs=element_divs,
        df_box_divs=json.dumps(df_box_divs),
        node_styles=node_styles,
        imported_drawflow=imported_drawflow,
    )
