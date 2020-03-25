// requirements.js
// script for 'requirements' endpoint
// SV: TODO

$(document).ready(function() {
	
	console.log('Page source loaded.')

	$(".req-input").change(function(){
		// If all requirements are checked
    	if ($('.req-input:checked').length == $('.req-input').length) {
    		// Show affirmative
       		$('.affirmative').css('display','flex')
       		$('.affirmative').focus()
       		// TODO: send to next view
    	} 
    	else {
    		// Hide affirmative
    		$('.affirmative').css('display','none')
    	}

	});

});