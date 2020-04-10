tutorial_content = document.getElementsByClassName("tutorial-content-container")[0];
tutorial_nav = document.getElementsByClassName("tutorial-nav-container")[0];
tutorial_sections = document.getElementsByClassName("tutorial-section");

$(document).ready(function() {
  $("#tutorial-nav-toggle").click(function() {
    toggleTutorialNav(this);
  });

  $(".logo a").click(function(e) {
    e.preventDefault();
    tutorial_content.scrollTop = tutorial_sections[0].offsetTop;
  })

  $("#tutorial-nav-back").click(function() {
    document.body.className = "fade"
    setTimeout(function() {
      window.location.href = "index";
    }, 500)
  })

  hljs.initHighlightingOnLoad();

  document.body.className = "";

  tutorial_content.classList.add(tutorial_content.getAttribute("data-anim"));
  tutorial_nav.classList.add(tutorial_nav.getAttribute("data-anim"));
})

function toggleTutorialNav(nav_button) {
  if ($(nav_button).hasClass("mdi-chevron-left")) {
    $(nav_button).removeClass("mdi-chevron-left");
    $(nav_button).addClass("mdi-chevron-right");

    $(".tutorial-nav-container").css("width", "0%")
    $(".tutorial-content-container").css("width", "100%")
  } else {
    $(nav_button).removeClass("mdi-chevron-right");
    $(nav_button).addClass("mdi-chevron-left");
    $(".tutorial-nav-container").css("width", "20%")
    $(".tutorial-content-container").css("width", "80%")
  }
}
