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
        "name": "div",
        "desc": "Division (SystemC)",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "opand1",
                "opand2",
            ],
            "outputs": ["data_out"],
        },
    },
    {
        "name": "sumsq",
        "desc": "Sum of squares (SystemC)",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "opand1",
                "opand2",
            ],
            "outputs": ["data_out"],
        },
    },
    {
        "name": "cacc",
        "desc": "Conditional accumulator (SystemC)",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "dist",
                "inner",
                "outer",
            ],
            "outputs": ["new_inner", "new_outer"],
        },
    },
    {
        "name": "mt19937",
        "desc": "Mersenne Twister PRNG (Verilog)",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "clk",
                "rst",
                "ready",
                "seed_val",
                "seed_start",
            ],
            "outputs": [
                "r_num",
                "valid",
                "busy",
            ],
        },
    },
    {
        "name": "swapprob",
        "desc": "Swap values on outcome (PyRTL)",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "input_list",
                "prob",
            ],
            "outputs": [
                "new_list",
            ],
        },
    },
    {
        "name": "collision",
        "desc": "Coordinate overlap (PyRTL)",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "h",
                "z",
                "d",
                "r",
            ],
            "outputs": [
                "new_h",
                "new_z",
                "new_d",
                "new_r",
            ],
        },
    },
    {
        "name": "gridwalk",
        "desc": "Walk grid subset (PyRTL)",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "subset",
                "grid",
            ],
            "outputs": [
                "new_grid",
            ],
        },
    },
    {
        "name": "prob",
        "desc": "Probability test (SystemC)",
        "param": {
            "clock": "1MHz",
            "link_speed": "1ps",
        },
        "links": {
            "inputs": [
                "p",
            ],
            "outputs": [
                "data_out",
            ],
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
            NODE_INPUT_STYLE.format(
                class_name=element_name, index=i + 1, value=j
            )
            for i, j in enumerate(element["links"]["inputs"])
        )
        node_styles += "\n".join(
            NODE_OUTPUT_STYLE.format(
                class_name=element_name, index=i + 1, value=j
            )
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
