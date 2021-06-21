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

HIDDEN_ELEMENT_DIV_TEMPL = """
<div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="__GROUP__" hidden>
  <i class="fas fa-code"></i><span> __GROUP__</span>
</div>
"""

DF_BOX_DIVS = {
    "__GROUP__": """<div class="dbclickbox" ondblclick="editor.changeModule('__GROUP__')">__GROUP__</div>"""
}
