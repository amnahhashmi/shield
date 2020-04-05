// health-and-safety.js

$(document).ready(function() {

	$('.icon').click(function(){
        var topnav = document.getElementById("topnav");
        if (topnav.className === "topnav") {
          topnav.className += " responsive";
        } else {
          topnav.className = "topnav";
        }
    });

	$('.home-link').click(function(){
		window.location.href = "home";
	})

	$('.health-and-safety-link').click(function(){
		window.location.replace("#top");

		var topnav = document.getElementById("topnav");
        if (topnav.className === "topnav") {
          return;
        } else {
          topnav.className = "topnav";
        }
	})

	$('.faq-link').click(function(){
		window.location.href = "home#above-faq";
	})

	$('.about-link').click(function(){
		window.location.href = "home#above-about";
	})

	$('.volunteer-button').click(function(){
		window.location.href = "volunteer";
	})
});