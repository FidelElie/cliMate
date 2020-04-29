// ! View Functions
function revealContent (objectsToAnimate) {
  document.body.className = "";
  objectsToAnimate.forEach(obj => {
    $(obj).addClass($(obj).attr("data-anim"));
  })
}

function hideContentAndNavigate(href) {
  document.body.className = "fade";
  setTimeout(() => {window.location.href = href;}, $("body, html").css("transiton"))
}

// ! Calucation Functions
function elemInView(window_top, element) {
  let window_mid = window_top + window.innerHeight / 2
  let element_top = element.offsetTop;
  let element_bottom = element_top + element.offsetHeight
  let in_view = element_bottom >= window_mid && window_mid >= element_top;
  return in_view
}

// ! Creation Functions
function createButton(text, class_value) {
  button = document.createElement("button");
  button.innerText = text;
  button.className = class_value;
  return button
}
