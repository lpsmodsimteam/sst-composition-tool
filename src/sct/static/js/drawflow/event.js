/* ---------------------- EVENTS ---------------------- */

/* ---------------------- NODE EVENTS ---------------------- */
editor.on("nodeCreated", function (id) {
  newNodeId = parseInt(id);
  nodeHistory[id] = newNodeId;
  console.log("Node added " + newNodeId);
});

editor.on("nodeRemoved", function (id) {
  // removedNodes = parseInt(id);
  console.log("Node removed " + id);
});

editor.on("nodeSelected", function (id) {
  if ($("#group_nodes").is(":checked") && !selectedNodes.includes(id)) {
    selectedNodes.push(id);
    $("#group_nodes_msg").text("Nodes selected " + selectedNodes);
  }
});
/* ---------------------- NODE EVENTS ---------------------- */

$("#group_nodes").change(function (e) {
  e.preventDefault();

  if ($("#group_nodes").is(":checked")) {
    $("#group_nodes_msg").text("In grouping mode");
  } else {
    $("#group_nodes_msg").text("");
    selectedNodes.length = 0;
  }
});

$("#export_button").click(function (e) {
  e.preventDefault();
  var drawflowData = editor.export();
  drawflowData["library"] = $("#library").val();
  drawflowData["element_list_html"] = $("#element_list").html();
  drawflowData["node_styles_html"] = $("#node_styles").html();
  drawflowData["df_box_divs"] = dfBoxDivs;
  $.post("/export", {
    drawflow_data: JSON.stringify(drawflowData),
  });
});

/* ---------------------- EVENTS ---------------------- */

function resetCreateComponent(numParams, numLinks) {
  $("#component_name").val("");
  $("#component_desc").val("");
  for (var i = 0; i < numParams; i++) {
    $("#remove_param").trigger("click");
  }
  for (var i = 0; i < numParams; i++) {
    $("#remove_link").trigger("click");
  }
}

function validateValue(value) {
  if ($.trim(value) == "") {
    return null;
  } else {
    return value;
  }
}

$("#create_component").click(function (e) {
  var name = validateValue($("#component_name").val());
  var desc = validateValue($("#component_desc").val());
  var $params = $("#component_params :input");
  var $links = $("#component_links :input");

  var paramValues = [];
  var paramKey = "";
  $params.each(function () {
    var valueId = $(this).attr("id");
    if (valueId.includes("value")) {
      paramKey = validateValue($(this).val());
    } else {
      paramValues.push({ [paramKey]: validateValue($(this).val()) });
    }
  });

  var paramHtml = "";
  for (const i in paramValues) {
    paramHtml += String.format(NODE_PARAM_HTML, Object.keys(paramValues[i])[0]);
  }

  var linkValues = { inputs: [], outputs: [] };
  var linkKey = "";
  $links.each(function () {
    var valueId = $(this).attr("id");
    if (valueId.includes("type")) {
      linkKey = validateValue($(this).val()) + "s";
    } else {
      linkValues[linkKey].push(validateValue($(this).val()));
    }
  });

  var nodeHtml = String.format(NEW_NODE_HTML, name, desc, paramHtml);

  dfBoxDivs[name] = {};
  dfBoxDivs[name]["html"] = nodeHtml;
  dfBoxDivs[name]["links"] = linkValues;
  dfBoxDivs[name]["param"] = paramValues;

  editor.addNode(
    name,
    linkValues["inputs"].length,
    linkValues["outputs"].length,
    width / 2,
    height / 2,
    name,
    { links: linkValues, param: paramValues },
    nodeHtml
  );

  var newNodeDivHtml = String.format(NEW_NODE_LIST_DIV_HTML, name);
  $(newNodeDivHtml).appendTo("#element_list");

  addModuleNodeStyles(name, [name]);

  resetCreateComponent(paramValues.length, linkValues.length);
});

$("#group_button").click(function (e) {
  if (selectedNodes.length) {
    var groupName = $("#group_nodes_name").val();

    if (groupName && !groupNamesSet.has(groupName)) {
      groupNamesSet.add(groupName);

      $("#group_nodes_msg").text("Created: " + groupName);
      editor.addModule(groupName);
      editor.changeModule(groupName);
      var newModuleDivHtml = String.format(NEW_MODULE_DIV_HTML, groupName);
      $(newModuleDivHtml).appendTo("#hierarchy");
      moveNodesToModule(groupName, selectedNodes);

      // reset variables and states
      selectedNodes.length = 0;
      groupedNum++;
      $("#group_nodes_name").val("group_name_" + groupedNum);
      $("#group_nodes").prop("checked", false);
    }
  }
});

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("node", ev.target.getAttribute("data-node"));
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("node");
  addNodeToDrawFlow(data, ev.clientX, ev.clientY);
}

function addNodeToDrawFlow(name, pos_x, pos_y) {
  if (editor.editor_mode === "fixed") {
    return false;
  }
  pos_x *= width / (width * editor.zoom);
  pos_x -=
    editor.precanvas.getBoundingClientRect().x *
    (width / (width * editor.zoom));
  pos_y *= height / (height * editor.zoom);
  pos_y -=
    editor.precanvas.getBoundingClientRect().y *
    (height / (height * editor.zoom));
  // console.log(dfBoxDivs);
  editor.addNode(
    name,
    dfBoxDivs[name]["links"]["inputs"].length,
    dfBoxDivs[name]["links"]["outputs"].length,
    pos_x,
    pos_y,
    name,
    { links: dfBoxDivs[name]["links"], param: dfBoxDivs[name]["param"] },
    dfBoxDivs[name]["html"]
  );
}

function changeModule(event) {
  var all = document.querySelectorAll(".menu ul li");
  for (var i = 0; i < all.length; i++) {
    all[i].classList.remove("selected");
  }
  event.target.classList.add("selected");
}
