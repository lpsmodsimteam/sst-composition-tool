$(document).ready(function () {
  var paramNum = 1;
  var addParamButton = $("#add_param"); //Add button selector
  var paramWrapper = $(".param_wrapper"); //Input param wrapper

  // once add button is clicked
  $(addParamButton).click(function () {
    var paramHtml = String.format(PARAM_HTML, paramNum, removeIconPngPath);
    $(paramWrapper).append(paramHtml); //Add param html
    paramNum++;
  });

  // once remove button is clicked
  $(paramWrapper).on("click", "#remove_param", function (e) {
    e.preventDefault();
    $(this).parent("div").remove(); //Remove param html
    paramNum--;
  });

  var linkNum = 1;
  var addLinkButton = $("#add_link"); //Add button selector
  var linkWrapper = $(".link_wrapper"); //Input link wrapper

  // once add button is clicked
  $(addLinkButton).click(function () {
    var linkHtml = String.format(LINK_HTML, linkNum, removeIconPngPath);
    $(linkWrapper).append(linkHtml); //Add link html
    linkNum++;
  });

  // once remove button is clicked
  $(linkWrapper).on("click", "#remove_link", function (e) {
    e.preventDefault();
    $(this).parent("div").remove(); //Remove link html
    linkNum--;
  });

  MicroModal.init({
    awaitCloseAnimation: true, // set to false, to remove close animation
    onShow: function (modal) {
      addModalContentHeight("short");
    },
  });
});

function addModalContentHeight(type) {
  var type = arguments[0] != null ? arguments[0] : "short";
  var modalContainer = $("#modal-container");
  var modalHeader = $("#modal-header");
  var modalContentContent = $("#modal-content-content");
  var modalContent = $("#modal-content");
  var modalFooter = $("#modal-footer");

  var modalIsDefined =
    modalContainer.length &&
    modalHeader.length &&
    modalContent.length &&
    modalFooter.length;

  if (modalIsDefined) {
    var modalContainerHeight = modalContainer.outerHeight();
    var modalHeaderHeight = modalHeader.outerHeight();
    var modalFooterHeight = modalFooter.outerHeight();

    var offset = 80;

    var height =
      modalContainerHeight - (modalHeaderHeight + modalFooterHeight + offset);

    if (!isNaN(height)) {
      height = height > 0 ? height : 20;

      if (type == "short") {
        modalContent.css({ height: height + "px" });
      } else {
        modalContainer.css({
          height: "100%",
          "overflow-y": "hidden",
          "margin-top": "40px",
        });
        modalContentContent.css({ height: "100%", "overflow-y": "auto" });
        modalContent.css({ "overflow-y": "visible" });
        modalFooter.css({ "margin-bottom": "120px" });
      }

      setTimeout(function () {
        modalContent.css({ display: "block" });
        var modalContentDOM = document.querySelector("#modal-content");
        modalContentDOM.scrollTop = 0;
      });
    }
  }
}

function showComponentModal(id) {
  MicroModal.show(id);
}

function showCreateComponentModal(id) {
  MicroModal.show(id);
}
