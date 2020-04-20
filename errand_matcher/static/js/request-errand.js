// request-errand.js
// script for 'request-errand' endpoint

$(document).ready(function() {
	var pages = $(".page")
	pageIndex = 0;

	// custom event for toggling between pages of errand form
	$("body").bind("pageEvent", function(e, index){

		// hide all pages
		$(pages).hide()

		// show desired page
		$(pages[index]).show()

		// set pageIndex to reflect shown page 
		pageIndex = index

	})

	// button behavior
	$(".next-button").click(function(){
		// TODO: Add POST to actually submit errand request.
		$('body').trigger("pageEvent", pageIndex + 1)
	})

	$(".back-button").click(function(){
		window.location.replace("home");
	})

	$(".health-and-safety-button").click(function(){
		window.location.replace("health");
	})

	$(".faq-button").click(function(){
		window.location.replace("home#above-faq");
	})

	$(".support-button").click(function(){
		window.location.replace("home#above-about");
	})

	// display first page
	$("body").trigger("pageEvent",0)
});
