DF_BOX_DIVS = """
<div>
  <div class="title-box">
    <i class="fas fa-code"></i> {element}
  </div>

  <div class="modal micromodal-slide" id="modal-{element}" aria-hidden="true">
    <div class="modal__overlay" tabindex="-1" data-micromodal-close>
    <div id="modal-container" class="modal__container" role="dialog" aria-modal="true" aria-labelledby="modal-{element}-title">
      <header id="modal-header" class="modal__header">
      <h2 class="modal__title">
        {element}: {desc}
      </h2>
      <button type="button" class="modal__close" aria-label="Close modal" data-micromodal-close></button>
      </header>
      <div id="modal-content-content" class="modal-content-content">
      <div id="modal-content" class="modal__content">
        {input_tag}
      </div>
      <footer id="modal-footer" class="modal__footer">
        <button type="button" class="modal__btn" data-micromodal-close aria-label="Close this dialog window">Close</button>
      </footer>
      </div>
    </div>
    </div>
  </div>

  <div class="box dbclickbox" id="modal-{element}" ondblclick="showComponentModal(this.id)">
    {desc}
  </div>
</div>
"""

INPUT_TAG = """<input type="text" df-{key} placeholder="{key}"><br>"""

ELEMENT_DIV = """
<div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="{0}">
  <i class="fas fa-code"></i><span> {0}</span>
</div>
"""

NODE_INPUT_STYLE = """
.drawflow-node.{class_name} .inputs .input:nth-child({index}):before {{
  display: block;
  content: "{value}";
  position: relative;
  right: 120px;
}}
"""

NODE_OUTPUT_STYLE = """
.drawflow-node.{class_name} .outputs .output:nth-child({index}):before {{
  display: block;
  content: "{value}";
  position: relative;
  left: 30px;
}}
"""
