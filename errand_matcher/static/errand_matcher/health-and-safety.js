// health-and-safety.js

$(document).ready(function() {

	$('.home-link').click(function(){
		window.location.href = "home";
	})

	$('.health-and-safety-link').click(function(){
		window.location.replace("#top");
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