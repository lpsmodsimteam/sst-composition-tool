/* -------------------- MODAL HTML -------------------- */
const PARAMHTML = `
<div>
  <input id="param_value_{0}" type="text" value=""/>
  <select id="param_type_{0}">
    <option value="str">str</option>
    <option value="int">int</option>
    <option value="list">list</option>
  </select>
  <a href="javascript:void(0);" id="remove_param" class="remove_button">
    <img src="{1}"/>
  </a>
</div>`;

const LINKHTML = `
<div>
  <select id="link_type_{0}">
    <option value="input">input</option>
    <option value="output">output</option>
  </select>
  <input id="link_label_{0}" type="text" value=""/>
  <a href="javascript:void(0);" id="remove_link" class="remove_button">
    <img src="{1}"/>
  </a>
</div>`;
/* -------------------- MODAL HTML -------------------- */

/* -------------------- STYLES -------------------- */
const IOSTYLE = `
.drawflow-node.{0} .{1} .{2}:nth-child({3}):before {
  display: block;
  content: "{4}";
  position: relative;
  {5}px;
}`;

const NEWELEMENTSTYLE = `
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
const NODEPARAMHTML = `<input type="text" df-{0} placeholder="{0}"><br>`;

const NEWNODEHTML = `
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

const NEWMODULEDIVHTML = `
<li onclick="editor.changeModule('{0}'); changeModule(event);">{0}</li>`;

const NEWGROUPLISTDIVHTML = `
<div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="{0}" style="background: #2c3e50; color: #1abc9c;">
  <i class="fas fa-code"></i><span> {0}</span>
</div>`;

const NEWNODELISTDIVHTML = `
<div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="{0}">
  <i class="fas fa-code"></i><span> {0}</span>
</div>`;

const NEWGROUPNODEHTML = `
  <div class="dbclickbox" ondblclick="editor.changeModule('{0}')">{0}</div>`;
/* -------------------- NODE HTML -------------------- */
