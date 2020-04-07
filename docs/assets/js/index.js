// ! Cached Selectors
footer = document.getElementsByClassName("footer")[0];
sections = document.getElementsByClassName("animated");


// ! Functions
$(document).ready(function() {

  document.body.className = ""

  $(".windows-button, .unix-button").click(function() {
    showPlatformCode(this)
  })

  $("#nav-arrow-opener, .scroll-link").click(function(e) {
    e.preventDefault();
    scrollToSection(this);
  })

  $(".title-card").click(function() {
    showExample(this);
  })

  $(".example-card").click(function() {
    copyToClipboard(this);
  })

  $(window).scroll(function() {
    let scroll_location = Math.ceil($(this).scrollTop());
    if (scroll_location > 25 && scroll_location < footer.offsetTop) {
      $(".navbar").addClass("background");
      $(".navbar").removeClass("dark");
    } else if (scroll_location == footer.offsetTop) {
      $(".navbar").removeClass("background")
      $(".navbar").addClass("dark")
    } else {
      $(".navbar").removeClass("background");
    }

    $(".animated").each(function() {
      if (elemInView(scroll_location, this) === true) {
        $(this).addClass($(this).attr("data-anim"));
      }
    })
  })

  $(".navbar-open").click(function() {
    document.getElementsByClassName("navbar-overlay")[0].style.width = "100%";
    document.getElementsByClassName("navbar-overlay")[0].style.opacity = "1";
    document.getElementsByClassName("navbar")[0].style.opacity = "0";
  })

  $(".navbar-close").click(function() {
    document.getElementsByClassName("navbar-overlay")[0].style.width = "0%";
    document.getElementsByClassName("navbar-overlay")[0].style.opacity = "0";
    document.getElementsByClassName("navbar")[0].style.opacity = "1";
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

  $(window).trigger("scroll");
})

//  ! Utility Functions

function elemInView(window_top, element, tolerance = 5) {
  let window_mid = window_top + window.innerHeight / 2
  // console.log(window_mid)

  let element_top = element.offsetTop;
  let element_bottom = element_top + element.offsetHeight

  // console.log(element_top);
  // console.log(element_bottom);

  // if (tolerance < 0 || tolerance > 100) {
  //   throw Error("Tolerance Is A Percentage Integer");
  // } else {
  //   p_tolerance = (tolerance / 100) + 1
  // }

  // console.log(element_bottom >= window_mid)
  // console.log(window_mid >= element_top)

  let in_view = element_bottom >= window_mid && window_mid >= element_top;


  // let in_view = element_bottom <= window_bottom * p_tolerance && element_top >= window_top * p_tolerance;

  return in_view
}

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
  document.getElementsByClassName("navbar-overlay")[0].style.width = "0%";
  document.getElementsByClassName("navbar-overlay")[0].style.opacity = "0";
  document.getElementsByClassName("navbar")[0].style.opacity = "1";
}

function showPlatformCode(pressed_toggler) {
  let togglers = Array.from($(".windows-button, .unix-button"));
  let displays = Array.from($(".windows-option, .unix-option"));

  let selected_toggler = document.getElementsByClassName("platform-button toggled")[0];

  if (selected_toggler != pressed_toggler) {
    let selected_index = togglers.indexOf(selected_toggler);
    let pressed_index = togglers.indexOf(pressed_toggler);

    togglers[selected_index].classList.toggle("toggled");
    togglers[pressed_index].classList.toggle("toggled");

    displays[selected_index].classList.toggle("hidden");
    displays[pressed_index].classList.toggle("hidden");
  }
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
}

function openOverlay(features_button) {
  let button_id = features_button.getAttribute("id");
  let overlay = document.getElementById(`${button_id}-overlay`);
  overlay.style.height = "100%";
  overlay.style.opacity = "1";
  $(`#${button_id}-overlay .overlay-container .gif-container`).css("opacity", "1");
  $(`#${button_id}-overlay .overlay-container .copy-container`).css("opacity", "1");
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
    card_inner.style.transform = ""
  }
}
