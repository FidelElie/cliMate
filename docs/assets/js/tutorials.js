// utilities.js used
// ! Cached Selectors
tutorial_content = $(".tutorial-container");
tutorial_nav = $(".tutorial-nav-container");
tutorial_sections = $(".tutorial-section");
tutorial_accordions = $(".tutorial-accordion");
platform_code_blocks = $(".cross-platform-code");

$(document).ready(function() {
  // * Creating Cross Platform Code Blocks
  let platform = navigator.platform;
  let toggled_index = platform == "Win32" ? 0 : 1;
  let untoggled_index = toggled_index == 1 ? 0 : 1;

  $(".cross-platform-code").each(function() {
    createCPCodeBlocks(this, toggled_index, untoggled_index)
  })

  // * Creating Code Progression Code Blocks

  $(".code-progression").each(function() {createCodeProgressions(this)})

  // * Create Accordion Blocks

  $(".tutorial-accordion").each(function() {createAccordions(this)})

  // * Creating Navigation Elements
  let section_mapping = createTutorialMap(Array.from(tutorial_sections));
  let tutorial_navigation = createTutorialNavigation(section_mapping);
  tutorial_nav.append(tutorial_navigation);

  // * Binding General Elements
  $("#tutorial-nav-toggle").click(function() {
    toggleTutorialNav(this);
  });

  $(".logo a").click(function(e) {
    e.preventDefault();
    animateNavigation(tutorial_sections[0])
  })

  $("#tutorial-nav-back").click(function() {hideContentAndNavigate("index");})

  $(".tutorial-link").click(function(e) {
    e.preventDefault();
    let href = $(this).attr("href");
    let corresponding_section = href.replace("#", "");
    let section = document.getElementById(corresponding_section);
    animateNavigation(section)
  })

  $(".subsection-collapse").click(function(e) {
    e.preventDefault();
    section = $(this).parent().parent()[0];
    tutorial_subsections = $(section).find(".tutorial-nav-subsections")[0];
    if (!$(this).hasClass("mdi-flip-v")) {
      $(this).addClass("mdi-flip-v");
      tutorial_subsections.classList.add("shown");
    } else {
      $(this).removeClass("mdi-flip-v");
      tutorial_subsections.classList.remove("shown");
    }
  })

  $(".folder").click(function() {
    let parent_node = $(this).parent();
    let content_node = parent_node.find(".contents");
    let folder_span = $(this).children(".mdi")[0];
    if (folder_span.classList.contains("mdi-folder-outline")) {
      $(folder_span).removeClass("mdi-folder-outline");
      $(folder_span).addClass("mdi-folder-open-outline");
      $(content_node).css("display", "flex")
    } else {
      $(folder_span).removeClass("mdi-folder-open-outline");
      $(folder_span).addClass("mdi-folder-outline");
      $(content_node).css("display", "none")
    }
  })

  hljs.initHighlightingOnLoad();
  revealContent([tutorial_content])
})

// ! Accordion Functions

function createAccordions(acc) {
  let accordion_header = $(acc).find(".accordion-header");
  let accordion_contents = $(acc).find(".accordion-contents");
  let accordion_indicator = $(accordion_header).find(".accordion-indicator");

  let span = document.createElement("span")
  span.classList.add("mdi", "mdi-chevron-down");

  accordion_indicator.append(span)
  accordion_contents.addClass("hidden");

  accordion_header.click(function() {
    if (!span.classList.contains("mdi-flip-v")) {
      accordion_contents.removeClass("hidden");
      span.classList.add("mdi-flip-v")
    } else {
      accordion_contents.addClass("hidden");
      span.classList.remove("mdi-flip-v")
    }
  })
}

// ! Code Progression Functions
function createCodeProgressions(code_block) {
  let code_button_container = $(code_block).find(".code-buttons");

  $(code_button_container).append(createButton("Before", "before-button"));
  $(code_button_container).append(createButton("After", "after-button"));
  $(code_button_container).append(createButton("Snippets", "snippet-button"));

  let code_buttons = $(code_block).find(".code-buttons").children();
  let before_code = $(code_block).find(".before-code");
  let after_code = $(code_block).find(".after-code");
  let snippet_code = $(code_block).find(".snippet-code");
  let code_blocks = [before_code, after_code, snippet_code]
  $(code_buttons[2]).addClass("selected");
  $(code_blocks[0]).addClass("hidden");
  $(code_blocks[1]).addClass("hidden");

  $(code_buttons).click(function () {
    let button_index = Array.from(code_buttons).indexOf(this);
    let selected = $(code_block).find(".code-buttons").find(".selected");
    let selected_index = Array.from(code_buttons).indexOf(selected[0]);
    if (button_index != selected_index) {
      $(code_buttons[selected_index]).removeClass("selected");
      $(code_buttons[button_index]).addClass("selected");
      $(code_blocks[selected_index]).addClass("hidden");
      $(code_blocks[button_index]).removeClass("hidden");
    }
  })
}

// ! Tutorial Navigation Creation Functions
function createTutorialMap(sections) {
  let section_map = {};
  for (let i = 0; i < sections.length; i++) {
    let section_data = {};
    let section_contents = $(sections[i]).children();
    let current_sections = Array.from($(section_contents).filter("[id]"));
    section_data["id"] = $(sections[i]).attr("id");
    section_data["title"] = section_contents[0].innerText;
    if (current_sections.length > 0) {
      section_data["subsections"] = createTutorialMap(current_sections);
    }
    else {
      section_data["subsections"] = {}
    }
    section_map[`${i}`] = section_data;
  }
  return section_map
}

function createTutorialNavigation(object_map) {
  let tutorial_sections = Object.entries(object_map);
  let tutorial_nav = document.createElement("div");
  tutorial_nav.classList.add("tutorial-nav")
  for (i in tutorial_sections) {
    const section_infomation = tutorial_sections[i][1]
    const subsection_information = section_infomation.subsections;
    subsection_presence = hasSubSections(subsection_information);
    let section = createSection(section_infomation, subsection_presence);
    if (subsection_presence) {
      let subsection = createSubSection(subsection_information);
      section.appendChild(subsection);
    }
    tutorial_nav.appendChild(section);
  }
  return tutorial_nav
}

function createSection(section_information, hasSubSections) {
  let section_element = document.createElement("div");
  section_element.classList.add("tutorial-nav-section")

  let title_element = document.createElement("div");
  title_element.classList.add("tutorial-nav-header");

  let title_a = document.createElement("a");
  title_a.setAttribute("href", `#${section_information.id}`);
  title_a.innerText = section_information.title;
  title_a.classList.add("tutorial-link");
  title_element.appendChild(title_a);

  if (hasSubSections) {
    let arrow_element = document.createElement("span");
    arrow_element.classList.add("subsection-collapse", "mdi", "mdi-chevron-down");
    title_element.appendChild(arrow_element);
  }

  section_element.appendChild(title_element);
  return section_element
}

function createSubSection(subsection_information) {
  let subsection_element = document.createElement("div");
  subsection_element.classList.add("tutorial-nav-subsections");
  subsections = Object.entries(subsection_information);
  for (i in subsections) {
    const sub_info = subsections[i][1];
    subsection_element.appendChild(createTutorialLink(sub_info.id, sub_info.title));
  }
  return subsection_element
}

function createTutorialLink(id, title) {
  let title_a = document.createElement("a");
  title_a.classList.add("tutorial-link");
  title_a.setAttribute("href", `#${id}`);
  title_a.innerText = title;
  return title_a
}

function hasSubSections(subsection_object) {
  return Object.entries(subsection_object).length > 0 ? true : false;
}

// ! Code Block Methods
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
  Array.from(platform_code_blocks).forEach(block => {
    if (code_block === block) {
      null
    } else {
      toggleCodeBlock(block);
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
// ! View Display Methods
function animateNavigation(section) {
  if (getNavigationToggleState("#tutorial-nav-toggle")) {
    $("#tutorial-nav-toggle").click()
  }

  $(tutorial_content).css("opacity", "0");
  setTimeout(function() {
    window.scrollTo(0, section.offsetTop);
    $(tutorial_content).css("opacity", "1");
  }, 500)
}

function toggleTutorialNav(nav_button) {
  let nav_max_width = $(tutorial_nav).css("max-width");

  if (!getNavigationToggleState(nav_button)) {
    $(nav_button).addClass("mdi-flip-h");
    $(".tutorial-nav-container").css("width", nav_max_width);
    setTimeout(function() {
      $(".tutorial-nav").css("opacity", "1");
    }, 250)
  } else {
    $(nav_button).removeClass("mdi-flip-h");
    $(".tutorial-nav").css("opacity", "0");
    setTimeout(() => {
      $(".tutorial-nav-container").css("width", "0");
    }, 250)
  }
}

// ! General Functions
function getNavigationToggleState(nav_button) {
  return $(nav_button).hasClass("mdi-flip-h")
}
