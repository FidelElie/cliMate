// utilities.js used
// ! Cached Selectors
navbar = $(".navbar")
navbar_overlay = $(".navbar-overlay");
footer = $(".footer-section");
example_titles = $(".example-local");
example_cards = $(".example-card");

// ! Functions
$(document).ready(function() {
  let platform_info = determinePlatform();

  $(".cross-platform-code").each(function() {
    createCPCodeBlocks(this, platform_info.t_index, platform_info.u_index)
  })

  $(".scroll-link").click(function(e) {
    e.preventDefault();
    scrollToSection(this);
  })

  $(".title-card").click(function() {showExample(this);})

  $(".example-card.enabled").click(function() {copyToClipboard(this);})

  $("#tutorial-button").click(() => {hideContentAndNavigate("tutorials")})

  $(window).scroll(function() {
    let scroll_location = Math.ceil($(this).scrollTop());
    if (scroll_location > 25 && scroll_location < footer.offset().top) {
      $(navbar).addClass("background");
      $(navbar).removeClass("dark");
    } else if (scroll_location == footer.offset().top) {
      $(navbar).removeClass("background")
      $(navbar).addClass("dark")
    } else {
      $(navbar).removeClass("background");
    }

    $(".animated").each(function() {
      if (elemInView(scroll_location, this)) {
        $(this).addClass($(this).attr("data-anim"));
      }
    })
  })

  $(".navbar-open").click(function() {
    $(navbar_overlay).css("width", "100%");
    $(navbar_overlay).css("opacity", "1");
    $(navbar).css("opacity", "0");
  })

  $(".navbar-close").click(function() {
    $(navbar_overlay).css("width", "0%");
    $(navbar_overlay).css("opacity", "0");
    $(navbar).css("opacity", "1")
  })

  $(".features-card").click(function(e) {
    e.preventDefault();
    openOverlay(this);
  })

  $(".overlay-close").click(function(e) {
    e.preventDefault();
    closeOverlay(this);
  })

  setInterval(flipTutorialsCard , 4000);

  // Reaveal website contents upon document ready.
  document.body.className = "";

  $(window).trigger("scroll");
})

// ! View Functions

function scrollToSection(link) {
  let link_href = link.getAttribute("href");
  let class_from_href = link_href.replace("#", "");
  let class_to_scroll = document.getElementsByClassName(class_from_href)[0];
  let distance_to_scroll = class_to_scroll.offsetTop;

  window.scroll({
    top: distance_to_scroll,
    left: 0,
    behavior: "smooth"
  });
  $(navbar_overlay).css("width", "0%");
  $(navbar_overlay).css("opacity", "0");
  $(navbar).css("opacity", "1");
}

function showExample(pressed_toggler) {
  let togglers = Array.from(document.getElementsByClassName("title-card"));
  let displays = Array.from(document.getElementsByClassName("example-card"));
  let selected_toggle = document.getElementsByClassName("title-card selected")[0];

  if (pressed_toggler != selected_toggle) {
    selected_index = togglers.indexOf(selected_toggle);
    pressed_index = togglers.indexOf(pressed_toggler);

    togglers[selected_index].classList.toggle("selected");
    togglers[pressed_index].classList.toggle("selected");

    displays[selected_index].classList.toggle("visible");
    displays[pressed_index].classList.toggle("visible");
  }
}

function copyToClipboard(display) {
  window.getSelection().selectAllChildren(display);
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  let example_index = Array.from(example_cards).indexOf(display);
  let corresponding_title = example_titles[example_index];
  let copied_message = $(corresponding_title).children(".copied-message");
  $(copied_message).css("opacity", "1");
  setTimeout(() => {$(copied_message).css("opacity", "0");}, 2000);
}

function openOverlay(features_button) {
  let button_id = features_button.getAttribute("id");
  let overlay = document.getElementById(`${button_id}-overlay`);
  overlay.style.height = "100%";
  overlay.style.opacity = "1";
  setTimeout(function() {
    $(`#${button_id}-overlay .overlay-container .gif-container`).css("opacity", "1");
    $(`#${button_id}-overlay .overlay-container .copy-container`).css("opacity", "1");
  }, 500);
}

function closeOverlay(close_button) {
  let button_id = close_button.getAttribute("id");
  let split_id = button_id.split("-");
  let truncated_id = (split_id.slice(0, 2)).join("-");
  let overlay = document.getElementById(`${truncated_id}-overlay`);
  $(`#${truncated_id}-overlay .overlay-container .gif-container`).css("opacity", "0");
  $(`#${truncated_id}-overlay .overlay-container .copy-container`).css("opacity", "0");
  overlay.style.height = "0%";
  overlay.style.opacity = "0";
}

function flipTutorialsCard() {
  let card_inner = document.getElementsByClassName("flip-card-inner")[0];
  if (card_inner.style.transform == "") {
    card_inner.style.transform = "rotateY(180deg)";
  } else {
    card_inner.style.transform = "";
  }
}
