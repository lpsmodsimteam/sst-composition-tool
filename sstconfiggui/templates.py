#!/usr/bin/env python
# -*- coding: utf-8 -*-

DF_BOX_DIVS_TEMPL = """
<div>
  <div class="title-box">
    <i class="fas fa-code"></i> {element}
  </div>
  <div class="box">
    {input_tag}
  </div>
</div>
"""

INPUT_TAG_TEMPL = """<input type="text" df-{key} placeholder="{key}">"""

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
