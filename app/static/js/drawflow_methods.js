/* ---------------------- EVENTS ---------------------- */

/* ---------------------- NODE EVENTS ---------------------- */
editor.on("nodeCreated", function(id) {
    // console.log("Node created " + id);
    newNodeId = parseInt(id);
    nodeHistory[id] = newNodeId;
})

editor.on("nodeRemoved", function(id) {
    // removedNodes = parseInt(id);
    // console.log("Node removed " + id);
})

editor.on("contextmenu", function(id) {
    // removedNodes = parseInt(id);
    // console.log("yo what " + id);
})

editor.on("nodeSelected", function(id) {
    if ($("#group_nodes").is(":checked") && !selectedNodes.includes(id)) {
        selectedNodes.push(id);
        $("#group_nodes_msg").text("Nodes selected " + selectedNodes);
    }
    // generateIODropdown(id, editor.getNodeFromId(id)["name"], "inputs");
});
/* ---------------------- NODE EVENTS ---------------------- */

$("#group_nodes").change(function(e) {
    e.preventDefault();

    if ($("#group_nodes").is(":checked")) {

        $("#group_nodes_msg").text("In grouping mode");

    } else if (selectedNodes.length) {

        var groupName = $("#group_nodes_name").val();

        if (groupName && !groupNamesSet.has(groupName)) {

            groupNamesSet.add(groupName);

            $("#group_nodes_msg").text("Created: " + groupName);
            editor.addModule(groupName);
            editor.changeModule(groupName);
            var newModuleDivHtml = "<li onclick=\"editor.changeModule('" + groupName +
                                   "'); changeModule(event);\">" + groupName + "</li>";
            $(newModuleDivHtml).appendTo("#hierarchy");
            moveNodesToModule(groupName, selectedNodes);

            // reset variables and states
            selectedNodes.length = 0;
            groupedNum++;
            $("#group_nodes_name").val('group_name_' + groupedNum);
        }
    }
});

$("#export_button").click(function(e) {
    e.preventDefault();
    $.post("/export_drawflow_data", {drawflow_data : JSON.stringify(editor.export())});
});
/* ---------------------- EVENTS ---------------------- */

function allowDrop(ev) { ev.preventDefault(); }

function drag(ev) { ev.dataTransfer.setData("node", ev.target.getAttribute("data-node")); }

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("node");
    addNodeToDrawFlow(data, ev.clientX, ev.clientY);
}

function addNodeToDrawFlow(name, pos_x, pos_y) {
    if (editor.editor_mode === "fixed") {
        return false;
    }
    pos_x = pos_x * (editor.precanvas.clientWidth / (editor.precanvas.clientWidth * editor.zoom)) -
            (editor.precanvas.getBoundingClientRect().x *
             (editor.precanvas.clientWidth / (editor.precanvas.clientWidth * editor.zoom)));
    pos_y =
        pos_y * (editor.precanvas.clientHeight / (editor.precanvas.clientHeight * editor.zoom)) -
        (editor.precanvas.getBoundingClientRect().y *
         (editor.precanvas.clientHeight / (editor.precanvas.clientHeight * editor.zoom)));
    // console.log("after", dfBoxDivs[name]["links"]);
    editor.addNode(name, dfBoxDivs[name]["links"]["inputs"].length,
                   dfBoxDivs[name]["links"]["outputs"].length, pos_x, pos_y, name,
                   {"links" : dfBoxDivs[name]["links"], "param" : dfBoxDivs[name]["param"]},
                   dfBoxDivs[name]["html"]);
}

function changeModule(event) {
    var all = document.querySelectorAll(".menu ul li");
    for (var i = 0; i < all.length; i++) {
        all[i].classList.remove("selected");
    }
    event.target.classList.add("selected");
}

function changeMode(option) {
    if (option == "lock") {
        lock.style.display = "none";
        unlock.style.display = "block";
    } else {
        lock.style.display = "block";
        unlock.style.display = "none";
    }
}

function moveConnectionsToModule(newConnectionsArr) {

    for (const i in newConnectionsArr) {

        const outputList = newConnectionsArr[i]["outputs"];
        for (const j in outputList) {

            var newOutputs = outputList[j]["connections"];
            if (newOutputs.length) {
                for (const k in newOutputs) {
                    editor.addConnection(nodeHistory[newConnectionsArr[i]["old_id"]],
                                         nodeHistory[newOutputs[k]["node"]], j,
                                         newOutputs[k]["output"]);
                }
            }
        }
    }
}

function addGroupNodesConnectionLabels(groupName, newNamesArr, io) {
    var ioStyles = "";
    var newNumIos = 0;
    for (const i in newNamesArr) {

        const ioArr = dfBoxDivs[newNamesArr[i]]["links"][io];
        // console.log(ioArr);
        for (var j = 0; j < ioArr.length; j++) {

            dfBoxDivs[groupName]["links"][io].push(ioArr[j]);
            ioStyles += `
.drawflow-node.` + groupName +
                        ` .` + io + ` .` + io.substring(0, io.length - 1) + `:nth-child(` +
                        (newNumIos + 1) + `):before {
  display: block;
  content: "` + ioArr[j] +
                        `";
  position: relative;
  ` + (io === "inputs" ? "right: 120" : "left: 30") +
                        `px;
}
                   `;
            newNumIos++;
        }
    }
    return ioStyles;
}

function updateIO(cb, elementName, io, ioName) {
    // console.log(cb, elementName, io, ioName);
    if (!cb.checked) {
    }
}

function generateIODropdown(id, elementName, io) {

    const ioList = dfBoxDivs[elementName]["links"][io];

    var checkboxes = $("#element_inputs");
    var options = '';
    for (var val in ioList) {
        options += '<input type="checkbox" onclick="updateIO(this, \'' + elementName + '\', \'' +
                   io + '\', \'' + ioList[val] + '\');" name="' + ioList[val] + '" checked/>' +
                   ioList[val] + '<br />';
    }
    // console.log(options);
    checkboxes.html(options);
}

function addGroupNodesStyles(groupName, newNamesArr) {

    dfBoxDivs[groupName]["links"] = {"inputs" : [], "outputs" : []};
    const inputStyles = addGroupNodesConnectionLabels(groupName, newNamesArr, "inputs");
    const outputStyles = addGroupNodesConnectionLabels(groupName, newNamesArr, "outputs");

    var newElementStyle = `<style type='text/css'>` + inputStyles + outputStyles + `
.drawflow-node.` + groupName +
                          ` {
  background: #2c3e50;
  text-align: center;
  color: #1abc9c;
}
  </style>
  `;
    $(newElementStyle).appendTo("head");
}

function moveNodesToModule(groupName, selectedNodes) {

    function mapNewLinks(arr, nodeId) {
        return arr.map(function(e) {
            e += "#" + nodeId;
            return e;
        });
    }

    var totalInputs = 0;
    var totalOutputs = 0;
    var minPosX = Infinity;
    var minPosY = Infinity;

    var newLinks = {"inputs" : [], "outputs" : []};
    var newParams = [];

    const newConnectionsArr = [];
    const newNamesArr = [];

    for (var i = 0; i < selectedNodes.length; i++) {

        // get node of current module
        var oldNode = editor.getNodeFromId(selectedNodes[i]);

        // expand values into variables
        var newName = oldNode["name"];
        var newInputs = oldNode["inputs"];
        var newOutputs = oldNode["outputs"];
        var newPosX = oldNode["pos_x"];
        var newPosY = oldNode["pos_y"];
        var newData = oldNode["data"];
        var newHTML = oldNode["html"];
        var numInputs = Object.keys(newInputs).length;
        var numOutputs = Object.keys(newOutputs).length;

        editor.removeNodeId("node-" + oldNode["id"]);
        editor.addNode(newName, numInputs, numOutputs, newPosX, newPosY, newName, newData, newHTML);
        nodeHistory[oldNode["id"]] = newNodeId;
        newConnectionsArr.push({"old_id" : oldNode["id"], "outputs" : newOutputs});

        newNamesArr.push(newName);
        totalInputs += numInputs;
        totalOutputs += numOutputs;
        minPosX = Math.min(minPosX, newPosX);
        minPosY = Math.min(minPosY, newPosY);

        newLinks["inputs"] =
            newLinks["inputs"].concat(mapNewLinks(newData["links"]["inputs"], newNodeId));
        newLinks["outputs"] =
            newLinks["outputs"].concat(mapNewLinks(newData["links"]["outputs"], newNodeId));
        newParams.push({[newName] : newData["param"]});
    }

    moveConnectionsToModule(newConnectionsArr);

    editor.changeModule("Home");
    var newElementDivHtml = `
  <div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="` +
                            groupName + `" style="background: #2c3e50; color: #1abc9c;">
  <i class="fas fa-code"></i><span> ` +
                            groupName + `</span>
  </div>
  `;
    $(newElementDivHtml).appendTo("#element_list");

    var newGroupNodeHTML = `
  <div class="dbclickbox" ondblclick="editor.changeModule('` +
                           groupName + `')">` + groupName + `</div>
  `;
    dfBoxDivs[groupName] = {};
    dfBoxDivs[groupName]["html"] = newGroupNodeHTML;
    dfBoxDivs[groupName]["links"] = newLinks;
    dfBoxDivs[groupName]["param"] = newParams;
    // console.log("before", dfBoxDivs[groupName]["links"]);
    editor.addNode(groupName, totalInputs, totalOutputs, minPosX, minPosY, groupName,
                   {"links" : newLinks, "param" : newParams}, newGroupNodeHTML);

    addGroupNodesStyles(groupName, newNamesArr);
}
