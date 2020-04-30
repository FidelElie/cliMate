// ! General View Functions
function determinePlatform() {
  let platform = navigator.platform;
  let toggled_index = platform == "Win32" ? 0 : 1;
  let untoggled_index = toggled_index == 1 ? 0 : 1

  return {t_index: toggled_index, u_index: untoggled_index}
}

// ! View Functions
function revealContent (objectsToAnimate) {
  document.body.className = "";
  objectsToAnimate.forEach(obj => {
    $(obj).addClass($(obj).attr("data-anim"));
  })
}

function hideContentAndNavigate(href) {
  document.body.className = "fade";
  setTimeout(() => {window.location.href = href;}, 500)
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

// * Code Block Methods
function createCPCodeBlocks(code_block, current_platform, other_platform) {
  let platforms = $(code_block).find(".platforms").children();
  let terminal = $(code_block).find(".terminal");
  let outputs = $(terminal).children();

  outputs[0].innerText = `...\\> ${outputs[0].innerText}`;
  outputs[1].innerText = `$ ${outputs[1].innerText}`;

  $(platforms[current_platform]).addClass("selected");
  $(outputs[other_platform]).addClass("hidden");

  $(platforms).click(function () {
    let button_index = Array.from(platforms).indexOf(this);
    let selected = $(code_block).find(".platforms").find(".selected");
    let selected_index = Array.from(platforms).indexOf(selected[0]);
    if (button_index != selected_index) {
      $(platforms[selected_index]).removeClass("selected");
      $(platforms[button_index]).addClass("selected");
      $(outputs[selected_index]).addClass("hidden")
      $(outputs[button_index]).removeClass("hidden");
      toggleAllBlocks(code_block);
    }
  })
}

function toggleAllBlocks(code_block) {
  $(".cross-platform-code").each(function() {
    if (code_block != this) {
      toggleCodeBlock(this)
    }
  })
}

function toggleCodeBlock(block) {
  let platforms = $(block).find(".platforms").children();
  let terminal = $(block).find(".terminal");
  let outputs = $(terminal).children();
  let selected = $(block).find(".platforms").find(".selected")[0];
  let selected_index = Array.from(platforms).indexOf(selected);
  let changed_index = selected_index == 1 ? 0 : 1;

  $(platforms[selected_index]).removeClass("selected");
  $(platforms[changed_index]).addClass("selected");
  $(outputs[selected_index]).addClass("hidden");
  $(outputs[changed_index]).removeClass("hidden");
}
