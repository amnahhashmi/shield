// index.js

$(document).ready(function() {

	$('.top-link').click(function(){
		window.location.replace("#top");
	})

	$('.faq-link').click(function(){
		window.location.replace("#above-faq");
	})

	$('.about-link').click(function(){
		window.location.replace("#above-about");
	})

	$('.volunteer-button').click(function(){
		window.location.href = "signup";
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
