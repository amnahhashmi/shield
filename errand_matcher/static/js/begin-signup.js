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

    // email validation - AH 4.06.2020 remove and deal with criminal
    // background in matching
    // AH 4.16.2020 validate email clientside

  $('#email-input').blur(function(e){
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    if (regex.test($('#email-input').val())) {
      // Hide warning and enable button
      $("#email-warning").hide()
      $('#send-confirmation-email-button').prop('disabled', false);
    } else {
      // Show warning and disable button
      $("#email-warning").show();
      $('#send-confirmation-email-button').prop('disabled', true);
    }
  });
});