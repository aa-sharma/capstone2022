import API from "./modules/api.js";

(function ($) {
  "use strict";
  var nav = $("nav");
  var navHeight = nav.outerHeight();
  $(".navbar-toggler").on("click", function () {
    if (!$("#mainNav").hasClass("navbar-reduce")) {
      $("#mainNav").addClass("navbar-reduce");
    }
  });

  // Preloader
  $(window).on("load", function () {
    if ($("#preloader").length) {
      $("#preloader")
        .delay(100)
        .fadeOut("slow", function () {
          $(this).remove();
        });
    }
  });

  // Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $(".back-to-top").fadeIn("slow");
    } else {
      $(".back-to-top").fadeOut("slow");
    }
  });
  $(".back-to-top").click(function () {
    $("html, body").animate({ scrollTop: 0 }, 0, "easeInExpo");
    return false;
  });

  $(".js-scroll").click(function () {
    $("html, body").animate({ scrollTop: 0 }, 0, "easeInExpo");
    return false;
  });

  // /*--/ Star ScrollTop /--*/
  // $(".scrolltop-mf").on("click", function () {
  //   $("html, body").animate(
  //     {
  //       scrollTop: 0,
  //     },
  //     1000
  //   );
  // });

  /*--/ Star Scrolling nav /--*/
  $('a.js-scroll[href*="#"]:not([href="#"])').on("click", function () {
    if (
      location.pathname.replace(/^\//, "") ==
        this.pathname.replace(/^\//, "") &&
      location.hostname == this.hostname
    ) {
      var target = $(this.hash);
      target = target.length ? target : $("[name=" + this.hash.slice(1) + "]");
      if (target.length) {
        $("html, body").animate(
          {
            scrollTop: target.offset().top - navHeight + 5,
          },
          1000,
          "easeInOutExpo"
        );
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $(".js-scroll").on("click", function () {
    $(".navbar-collapse").collapse("hide");
  });

  // Activate scrollspy to add active class to navbar items on scroll
  // $("body").scrollspy({
  //   target: "#mainNav",
  //   offset: navHeight,
  // });
  /*--/ End Scrolling nav /--*/

  /*--/ Navbar Menu Reduce /--*/
  $(window).trigger("scroll");
  $(window).on("scroll", function () {
    var pixels = 50;
    var top = 1200;
    if ($(window).scrollTop() > pixels) {
      $(".navbar-expand-md").addClass("navbar-reduce");
      $(".navbar-expand-md").removeClass("navbar-trans");
    } else {
      $(".navbar-expand-md").addClass("navbar-trans");
      $(".navbar-expand-md").removeClass("navbar-reduce");
    }
    if ($(window).scrollTop() > top) {
      $(".scrolltop-mf").fadeIn(1000, "easeInOutExpo");
    } else {
      $(".scrolltop-mf").fadeOut(1000, "easeInOutExpo");
    }
  });

  /*--/ Star Typed /--*/
  if ($(".text-slider").length == 1) {
    var typed_strings = $(".text-slider-items").text();
    var typed = new Typed(".text-slider", {
      strings: typed_strings.split(","),
      typeSpeed: 80,
      loop: true,
      backDelay: 1100,
      backSpeed: 30,
    });
  }

  /*--/ Testimonials owl /--*/
  $("#testimonial-mf").owlCarousel({
    margin: 20,
    autoplay: true,
    autoplayTimeout: 4000,
    autoplayHoverPause: true,
    responsive: {
      0: {
        items: 1,
      },
    },
  });
})(jQuery);

const token = localStorage["token"];
const loggedInElements = document.getElementsByClassName("logged-in");
const notLoggedInElements = document.getElementsByClassName("not-logged-in");

const unauthorizedPaths = [
  "/my-account.html",
  "/exercises.html",
  "/dashboard.html",
];

const fetchUser = async () => {
  if (!token) {
    if (unauthorizedPaths.includes(window.location.pathname)) {
      // logged out user is in authorized location, reassign to home page
      window.location.assign("/");
    }

    // user is logged out
    return false;
  }

  const api = new API({ url: "/api/auth", token });
  const { res, json } = await api.call();

  if (res.status != 200) {
    // token is not valid, remove it and reassign to home page
    localStorage.removeItem("token");
    window.location.assign("/");
  }

  // user is valid
  return true;
};

if (await fetchUser()) {
  // user is logged in
  for (let notLoggedInElement of notLoggedInElements) {
    notLoggedInElement.classList.add("d-none");
  }

  const signoutEl = document.getElementById("sign-out");
  signoutEl.addEventListener("click", () => {
    localStorage.removeItem("token");
  });
} else {
  // user is not logged in
  for (let loggedInElement of loggedInElements) {
    loggedInElement.classList.add("d-none");
  }
}
