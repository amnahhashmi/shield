// begin-signup.js
// script for 'requirements' endpoint
// SV: TODO

$(document).ready(function() {

	$('#reqs-page').css('display','block')

	$(".req-input").change(function(){
		// If all requirements are checked
    	if ($('.req-input:checked').length == $('.req-input').length) {

    		// Show affirmative
       		$('.affirmative').css('display','flex')
       		$('.affirmative').focus()

       		window.setTimeout(function(){
       			// Change page displayed
	       		$('#reqs-page').css('display', 'none')
	       		$('#email-page').css('display', 'block')

	       		// Activate back button
	       		$('#back-button').removeClass('disabled')
	       		$('#back-button').children().addBack().click(function(){
	       			$('#email-page').css('display', 'none')
	       			$('#reqs-page').css('display', 'block')
	       			$('#back-button').addClass('disabled')
	       		});
       		}, 2000)
    	} 
    	else {
    		// Hide affirmative
    		$('.affirmative').css('display','none')
    	}

	});

});