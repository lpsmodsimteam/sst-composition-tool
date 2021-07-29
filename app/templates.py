#!/usr/bin/env python
# -*- coding: utf-8 -*-

DF_BOX_DIVS_TEMPL = """
<div>
  <div class="title-box">
    <i class="fas fa-code"></i> {element}
  </div>
  <div class="box dbclickbox" ondblclick="showpopup(event)">
    {desc}
    <div class="modal" style="display:none">
      <div class="modal-content">
        <span class="close" onclick="closemodal(event)">&times;</span>
        {input_tag}
      </div>
    </div>
  </div>
</div>
"""

INPUT_TAG_TEMPL = """<input type="text" df-{key} placeholder="{key}"><br>"""

ELEMENT_DIV_TEMPL = """
<div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="{0}">
  <i class="fas fa-code"></i><span> {0}</span>
</div>
"""

DF_BOX_DIVS = {}

NODE_INPUT_STYLE_TEMPL = """
.drawflow-node.{class_name} .inputs .input:nth-child({index}):before {{
  display: block;
  content: "{value}";
  position: relative;
  right: 120px;
}}
"""

NODE_OUTPUT_STYLE_TEMPL = """
.drawflow-node.{class_name} .outputs .output:nth-child({index}):before {{
  display: block;
  content: "{value}";
  position: relative;
  left: 30px;
}}
"""

COMPONENT_INIT_TEMPL = """{name} = sst.Component("{name}", "{library}.{class_name}")"""
COMPONENT_PARAM_TEMPL = "{name}.addParams({params})"
COMPONENT_LINK_TEMPL = """sst.Link("{comp1}-{link1}").connect(
    ({comp1}, "{link1}", LINK_DELAY), ({comp2}, "{link2}", LINK_DELAY)
)"""


EXAMPLE_COMPONENTS = [
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
