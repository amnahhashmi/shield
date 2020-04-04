// begin-signup.js
// script for 'begin_signup' endpoint

$(document).ready(function() {

	$('#reqs-page').css('display','block')

	$(".req-input").change(function(){
		// If all requirements are checked
    	if ($('.req-input:checked').length == $('.req-input').length) {

    		// Show acknowledge
       		$('.acknowledge').css('display','flex')
       		$('.acknowledge').focus()
       	}
       	else {

       		// Hide affirmative and acknowledge
       		$('.acknowledge').css('display', 'none')
       		$('.affirmative').css('display','none')
       	}
    });

    $(".acknowledge-input").change(function(){
    	if ($('.acknowledge-input:checked')) {

    		// show affirmative
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
    		// hide affirmative
    		$('.affirmative').css('display','none')
    	}
    });

    // email validation
	$('#email-input').blur(function(e){
		if ($('#email-input').val().indexOf('.edu') >= 0) {
			// Enable button
			$('#send-confirmation-email-button').prop('disabled', false);
		} else {
			// Show warning
			$("#email-warning").show();
		}
	});
});