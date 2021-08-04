var PARAMHTML = `<div>
    <input id="param_label_{0}" type="text" value=""/>
    <select id="param_value_{0}">
        <option value="str">str</option>
        <option value="int">int</option>
        <option value="list">list</option>
    </select>
    <a href="javascript:void(0);" id="remove_param" class="remove_button">
        <img src="{1}"/>
    </a>
    </div>`;

var LINKHTML = `<div>
    <input id="link_label_{0}" type="text" value=""/>
    <select id="link_value_{0}">
        <option value="input">input</option>
        <option value="output">output</option>
    </select>
    <a href="javascript:void(0);" id="remove_link" class="remove_button">
        <img src="{1}"/>
    </a>
    </div>`;

var IOSTYLE = `
.drawflow-node.{0} .{1} .{2}:nth-child({3}):before {
  display: block;
  content: "{4}";
  position: relative;
  {5}px;
}`;
