function addNodeConnectionLabels(moduleName, newNamesArr, io) {
  var ioStyles = "";
  var newNumIos = 0;
  for (const i in newNamesArr) {
    const ioArr = dfBoxDivs[newNamesArr[i]]["links"][io];
    for (var j = 0; j < ioArr.length; j++) {
      ioStyles += String.format(
        IO_STYLE,
        moduleName,
        io,
        io.substring(0, io.length - 1),
        newNumIos + 1,
        ioArr[j],
        io === "inputs" ? "right: 120" : "left: 30"
      );

      newNumIos++;
    }
  }
  return ioStyles;
}

function addModuleNodeStyles(moduleName, newNamesArr) {
  const inputStyles = addNodeConnectionLabels(
    moduleName,
    newNamesArr,
    "inputs"
  );
  const outputStyles = addNodeConnectionLabels(
    moduleName,
    newNamesArr,
    "outputs"
  );

  var newElementStyle = String.format(
    NEW_MODULE_NODE_STYLE,
    inputStyles + outputStyles,
    moduleName
  );
  $(newElementStyle).appendTo("#node_styles");
}

function recomputeNodes(selectedNodes) {
  function mapNewLinks(arr, nodeId) {
    return arr.map(function (e) {
      e += "#" + nodeId;
      return e;
    });
  }
  var totalInputs = 0;
  var totalOutputs = 0;
  var minPosX = Infinity;
  var minPosY = Infinity;
  var newLinks = { inputs: [], outputs: [] };
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
    editor.addNode(
      newName,
      numInputs,
      numOutputs,
      newPosX,
      newPosY,
      newName,
      newData,
      newHTML
    );
    nodeHistory[oldNode["id"]] = newNodeId;
    newConnectionsArr.push({ old_id: oldNode["id"], outputs: newOutputs });

    newNamesArr.push(newName);
    totalInputs += numInputs;
    totalOutputs += numOutputs;
    minPosX = Math.min(minPosX, newPosX);
    minPosY = Math.min(minPosY, newPosY);

    newLinks["inputs"] = newLinks["inputs"].concat(
      mapNewLinks(newData["links"]["inputs"], newNodeId)
    );
    newLinks["outputs"] = newLinks["outputs"].concat(
      mapNewLinks(newData["links"]["outputs"], newNodeId)
    );
    newParams.push({ [newName]: newData["param"] });
  }

  return [
    newNamesArr,
    newConnectionsArr,
    newLinks,
    newParams,
    totalInputs,
    totalOutputs,
    minPosX,
    minPosY,
  ];
}

function moveConnectionsToModule(newConnectionsArr) {
  for (const i in newConnectionsArr) {
    const outputList = newConnectionsArr[i]["outputs"];
    for (const j in outputList) {
      var newOutputs = outputList[j]["connections"];
      if (newOutputs.length) {
        for (const k in newOutputs) {
          editor.addConnection(
            nodeHistory[newConnectionsArr[i]["old_id"]],
            nodeHistory[newOutputs[k]["node"]],
            j,
            newOutputs[k]["output"]
          );
        }
      }
    }
  }
}

function addModuleHtml(moduleName) {
  var newElementDivHtml = String.format(NEW_MODULE_LIST_DIV_HTML, moduleName);
  $(newElementDivHtml).appendTo("#element_list");
}

function addNewModuleNode(
  moduleName,
  newLinks,
  newParams,
  totalInputs,
  totalOutputs,
  minPosX,
  minPosY
) {
  var newGroupNodeHTML = String.format(NEW_MODULE_NODE_HTML, moduleName);

  dfBoxDivs[moduleName] = {};
  dfBoxDivs[moduleName]["html"] = newGroupNodeHTML;
  dfBoxDivs[moduleName]["links"] = newLinks;
  dfBoxDivs[moduleName]["param"] = newParams;
  editor.addNode(
    moduleName,
    totalInputs,
    totalOutputs,
    minPosX,
    minPosY,
    moduleName,
    { links: newLinks, param: newParams },
    newGroupNodeHTML
  );
}

function moveNodesToModule(moduleName, selectedNodes) {
  // compute values of nodes created in the module
  const [
    newNamesArr,
    newConnectionsArr,
    newLinks,
    newParams,
    totalInputs,
    totalOutputs,
    minPosX,
    minPosY,
  ] = recomputeNodes(selectedNodes);

  // move values of node connections into the module view
  moveConnectionsToModule(newConnectionsArr);

  editor.changeModule("Home");
  // add module to ELEMENT_LIST
  addModuleHtml(moduleName);

  // add module as a node to the global map and canvas
  addNewModuleNode(
    moduleName,
    newLinks,
    newParams,
    totalInputs,
    totalOutputs,
    minPosX,
    minPosY
  );

  // add styles for the newly created nodes in the module
  addModuleNodeStyles(moduleName, newNamesArr);
}
