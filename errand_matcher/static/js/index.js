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

	$('.top-link').click(function(){
		window.location.replace("#top");
	})

	$('.health-and-safety-link').click(function(){
		window.location.href = "health";
	})

	$('.faq-link').click(function(){
		window.location.replace("#above-faq");
		collapseTopNav();
	})

	$('.about-link').click(function(){
		window.location.replace("#above-about");
		collapseTopNav();
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
		window.location.href = "volunteer/signup";
	})

	$('.requestor-button').click(function(){
		window.location.href = "requestor";
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
