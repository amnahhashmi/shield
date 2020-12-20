// index.js

$(document).ready(function() {

	$('.icon').click(function(){
        var topnav = document.getElementById("topnav");
        if (topnav.className === "topnav") {
          topnav.className += " responsive";
        } else {
          topnav.className = "topnav";
        }
    });

    // navbar button behavior
	var home_url;
	if (location.port) {
		home_url = window.location.protocol +'//' + document.domain + ':' + location.port;
	} else {
		home_url = window.location.protocol +'//' + document.domain;
	}

	$('.top-link').click(function(){
		window.location.href = home_url + "#top";
	})

	$('.health-and-safety-link').click(function(){
		window.location.href = home_url + "/health";
	})

	$('.faq-link').click(function(){
		window.location.href = home_url + "#above-faq";
	})

	$('.about-link').click(function(){
		window.location.href = home_url + "#above-about";
	})

	$('.partners-link').click(function(){
		window.location.href = home_url + "/partner";
	})

	$('.volunteer-login-link').click(function(){
		window.location.href = home_url + "/volunteer/login/";
	})



	function collapseTopNav() {
		var topnav = document.getElementById("topnav");
        if (topnav.className === "topnav") {
          return;
        } else {
          topnav.className = "topnav";
        }
	}

	$('.volunteer-button').click(function(){
		window.location.href = home_url + "/volunteer/signup";
	})

	$('.requestor-button').click(function(){
		window.location.href = home_url + "/requestor";
	})

	$('.collapsible').click(function(){
		this.classList.toggle("active");
		var image = $(this).find("img");
		var content = this.nextElementSibling;
        if (content.style.maxHeight) {
          content.style.maxHeight = null;
          image.css('transform','rotate(0deg)');
        } else {
          content.style.maxHeight = content.scrollHeight + "px";
          image.css('transform','rotate(-180deg)');
        }
	})
});
