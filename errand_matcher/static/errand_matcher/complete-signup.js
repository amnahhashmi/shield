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

		$("stop").slice(1,3).attr("offset",progressBarLocation)

		// todo handle button activation/deactivation
	})

	// button behavior
	$(".next-button").click(function(){
		$('body').trigger("pageEvent", pageIndex + 1)
	})


	$(".back-button").click(function(){
		if (pageIndex == 0) {
			// send to landing page
		} else {
			$('body').trigger("pageEvent", pageIndex - 1)
		}
	})

	// If all name input fields are full on blur/defocus, automatically progress
	$('#name-page').find(".text-input").blur(function(e){
		if ($('#firstname-input').val().length > 0 && $('#lastname-input').val().length > 0){
			// Set review field to user input
			$('#name-review').text($('#firstname-input').val() + ' ' + $('#lastname-input').val());

			$('body').trigger("pageEvent", pageIndex + 1)
		}
	});

	// phone input cleaning + validation 
	$('#phone-input').blur(function(e){
		phone = $(this).val();
		phone = phone.replace(/[^0-9]/g,'');

		$(this).val(
			(phone.slice(0,3) ? "("+phone.slice(0,3)+")" : "") +
			(phone.slice(3,6) ? "-"+phone.slice(3,6) : "") +
			(phone.slice(6,10) ? "-"+phone.slice(6,10) : "")
		);

		if (phone.length==10) {
			// Set review field to user input
			$('#phone-review').text(phone);
			$('body').trigger("pageEvent", pageIndex + 1)
		} else {
			// display a warning message
		}
	})
	
	// display first page
	$("body").trigger("pageEvent",0)

});