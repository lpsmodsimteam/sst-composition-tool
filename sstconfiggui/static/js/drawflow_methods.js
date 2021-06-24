/* DRAG EVENTS */
/* Mouse and Touch Actions */
var elements = $(".drag-drawflow");

for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener("touchend", drop, false);
    elements[i].addEventListener("touchstart", drag, false);
}

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
    editor.addNode(name, dfBoxDivs[name]["link"]["input"].length,
                   dfBoxDivs[name]["link"]["output"].length, pos_x, pos_y, name, {},
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

/* ---------------------- NODE EVENTS ---------------------- */
editor.on("nodeCreated", function(id) {
    console.log("Node created " + id);
    newNodeId = parseInt(id);
    oldToNewNodeMap[id] = newNodeId;
})

editor.on("nodeRemoved", function(id) {
    // removedNodes = parseInt(id);
    console.log("Node removed " + id);
})

editor.on("contextmenu", function(id) {
    // removedNodes = parseInt(id);
    console.log("yo what " + id);
})

editor.on("nodeSelected", function(id) {
    console.log(id);
    if ($("#group_nodes").is(":checked") && !selectedNodes.includes(id)) {
        selectedNodes.push(id);
        $("#group_nodes_msg").text("Nodes selected " + selectedNodes);
    }
});
/* ---------------------- NODE EVENTS ---------------------- */

$("#export_button").click(function(e) {
    e.preventDefault();
    $.post("/export_drawflow_data", {drawflow_data : JSON.stringify(editor.export())});
});

function moveConnectionsToModule(newConnections) {

    for (const i in newConnections) {

        for (const j in newConnections[i]["outputs"]) {
            var newOutputs = newConnections[i]["outputs"][j]["connections"];
            if (newOutputs.length) {
                for (const k in newOutputs) {
                    editor.addConnection(oldToNewNodeMap[newConnections[i]["old_id"]],
                                         oldToNewNodeMap[newOutputs[k]["node"]], j,
                                         newOutputs[k]["output"]);
                }
            }
        }
    }
}

function moveNodesToModule(groupName, selectedNodes) {

    var totalInputs = 0;
    var totalOutputs = 0;
    var minPosX = Infinity;
    var minPosY = Infinity;

    const newConnections = [];

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
        oldToNewNodeMap[oldNode["id"]] = newNodeId;
        newConnections.push({"old_id" : oldNode["id"], "outputs" : newOutputs});

        totalInputs += numInputs;
        totalOutputs += numOutputs;
        minPosX = Math.min(minPosX, newPosX);
        minPosY = Math.min(minPosY, newPosY);
    }

    moveConnectionsToModule(newConnections);

    editor.changeModule("Home");

    var newElementDivHtml = `
    <div class="drag-drawflow" draggable="true" ondragstart="drag(event)" data-node="` +
                            groupName + `">
    <i class="fas fa-code"></i><span> ` +
                            groupName + `</span>
    </div>
    `;
    $(newElementDivHtml).appendTo("#element_list");

    var newGroupNodeHTML = `
    <div class="dbclickbox" ondblclick="editor.changeModule('` +
                           groupName + `')">` + groupName + `</div>
    `;
    dfBoxDivs[groupName] = newGroupNodeHTML;
    editor.addNode(groupName, totalInputs, totalOutputs, minPosX, minPosY, groupName, {},
                   newGroupNodeHTML);
}

$("#group_nodes").change(function(e) {
    e.preventDefault();

    if ($("#group_nodes").is(":checked")) {

        $("#group_nodes_msg").text("In grouping mode");

    } else if (selectedNodes.length) {

        var groupName = $("#group_nodes_name").val();

        if (groupName) {

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
})
