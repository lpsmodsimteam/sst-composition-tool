var transform = '';
function showpopup(e) {
    console.log(e);
  e.target.closest(".drawflow-node").style.zIndex = "9999";
  e.target.children[0].style.display = "block";
  //document.getElementById("modalfix").style.display = "block";

  //e.target.children[0].style.transform = 'translate('+translate.x+'px, '+translate.y+'px)';
  transform = editor.precanvas.style.transform;
  editor.precanvas.style.transform = '';
  editor.precanvas.style.left = editor.canvas_x +'px';
  editor.precanvas.style.top = editor.canvas_y +'px';
  console.log(transform);

  //e.target.children[0].style.top  =  -editor.canvas_y - editor.container.offsetTop +'px';
  //e.target.children[0].style.left  =  -editor.canvas_x  - editor.container.offsetLeft +'px';
  editor.editor_mode = "fixed";

}

 function closemodal(e) {
   e.target.closest(".drawflow-node").style.zIndex = "2";
   e.target.parentElement.parentElement.style.display  ="none";
   //document.getElementById("modalfix").style.display = "none";
   editor.precanvas.style.transform = transform;
     editor.precanvas.style.left = '0px';
     editor.precanvas.style.top = '0px';
    editor.editor_mode = "edit";
 }