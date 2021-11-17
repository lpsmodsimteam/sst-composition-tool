/* -------------------- MODAL HTML -------------------- */
const PARAM_HTML = `
<div>
  <input id="param_value_{0}" type="text" value="param{0}"/>
  <select id="param_type_{0}">
    <option value="str">str</option>
    <option value="int">int</option>
    <option value="list">list</option>
  </select>
  <a href="javascript:void(0);" id="remove_param" class="remove_button">
    <img src="{1}"/>
  </a>
</div>`;

const LINK_HTML = `
<div>
  <select id="link_type_{0}">
    <option value="input">input</option>
    <option value="output">output</option>
  </select>
  <input id="link_label_{0}" type="text" value="link{0}"/>
  <a href="javascript:void(0);" id="remove_link" class="remove_button">
    <img src="{1}"/>
  </a>
</div>`;

/* -------------------- MODAL HTML -------------------- */

/* -------------------- STYLES -------------------- */
const IO_STYLE = `
.drawflow-node.{0} .{1} .{2}:nth-child({3}):before {
  display: block;
  content: "{4}";
  position: relative;
  {5}px;
}`;

const NEW_MODULE_NODE_STYLE = `
<style type='text/css'>
  {0}
  .drawflow-node.{1} {
    background: #2c3e50;
    text-align: center;
    color: #1abc9c;
  }
</style>`;
/* -------------------- STYLES -------------------- */

/* -------------------- NODE HTML -------------------- */
const NODE_PARAM_HTML = `<input type="text" df-{0} placeholder="{0}"><br>`;

const NEW_NODE_HTML = `
<div>
  <div class="title-box">
    <i class="fas fa-code"></i> {0}
  </div>

  <div class="modal micromodal-slide" id="modal-{0}" aria-hidden="true">
    <div class="modal__overlay" tabindex="-1" data-micromodal-close>
    <div id="modal-container" class="modal__container" role="dialog" aria-modal="true" aria-labelledby="modal-{0}-title">
      <header id="modal-header" class="modal__header">
      <h2 class="modal__title">
        {0}: {1}
      </h2>
      <button type="button" class="modal__close" aria-label="Close modal" data-micromodal-close></button>
      </header>
      <div id="modal-content-content" class="modal-content-content">
      <div id="modal-content" class="modal__content">
        {2}
      </div>
      <footer id="modal-footer" class="modal__footer">
        <button type="button" class="modal__btn" data-micromodal-close aria-label="Close this dialog window">Close</button>
      </footer>
      </div>
    </div>
    </div>
  </div>

  <div class="box dbclickbox" id="modal-{0}" ondblclick="showComponentModal(this.id)">
    {1}
  </div>
</div>`;

const NEW_MODULE_DIV_HTML = `
<li onclick="editor.changeModule('{0}'); changeModule(event);">{0}</li>`;

const NEW_MODULE_LIST_DIV_HTML = `
<div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="{0}" style="background: #2c3e50; color: #1abc9c;">
  <i class="fas fa-code"></i><span> {0}</span>
</div>`;

const NEW_NODE_LIST_DIV_HTML = `
<div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="{0}">
  <i class="fas fa-code"></i><span> {0}</span>
</div>`;

const NEW_MODULE_NODE_HTML = `
  <div class="dbclickbox" ondblclick="editor.changeModule('{0}')">{0}</div>`;
/* -------------------- NODE HTML -------------------- */
