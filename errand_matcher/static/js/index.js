// index.js

$(document).ready(function() {

	$('.icon').click(function(){
        var topnav = document.getElementById("topnav");
        if (topnav.className === "topnav") {
          topnav.className += " responsive";
        } else {
          topnav.className = "topnav";
        }
        $(topnav).next().css("margin-top",topnav.scrollHeight);
    });

	$('.top-link').click(function(){
		window.location.href ="/#top";
	})

	$('.health-and-safety-link').click(function(){
		window.location.href = "/health";
	})

	$('.faq-link').click(function(){
		window.location.href = "/#above-faq";
	})

	$('.about-link').click(function(){
		window.location.href = "/#above-about";
	})

	function collapseTopNav() {
		var topnav = document.getElementById("topnav");
        if (topnav.className === "topnav") {
          return;
        } else {
          topnav.className = "topnav";
        }
	}

	$('#request-button').click(function(){
		// SV 4/11/20 : Should be a link to request page once that exists
		// window.location.href = "?";
	})

	$('#faq-button').click(function(){
		window.location.href = "/#above-faq";
	})

	$('#support-button').click(function(){
		// SV 4/11/20 : Should be a link to support page once that exists
		window.location.href = "/#above-about";
	})


});
