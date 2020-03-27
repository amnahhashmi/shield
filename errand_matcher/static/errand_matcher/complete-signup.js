// complete-signup.js
// script for 'begin_signup' endpoint

$(document).ready(function() {

	var pages = $(".page")
	var pageIndex = 0

	// custom event for toggling between pages of signup form
	$("body").bind("pageEvent", function(e, index){

		// hide all pages
		$(pages).hide()

		// show desired page
		$(pages[index]).show()

		// set pageIndex to reflect shown page 
		pageIndex = index

		// update progress bar
		progressBarLocation = (3 + pageIndex)/ pages.length
		console.log(progressBarLocation)
		console.log(pageIndex)
		$("stop").slice(1,3).attr("offset",progressBarLocation)

		// todo handle button activation/deactivation
	})

	$(".next-button").click(function(){
		// todo form validation
		$('body').trigger("pageEvent", pageIndex + 1)
	})

	$(".back-button").click(function(){
		if (pageIndex == 0) {
			// send to landing page
		} else {
			$('body').trigger("pageEvent", pageIndex - 1)
		}
	})
	
	// display first page
	$("body").trigger("pageEvent",0)

});