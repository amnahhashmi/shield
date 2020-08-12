// password-reset.js
// script for 'partner-password-reset-confirm' endpoint

$(document).ready(function() {
	// password validation
	$("#password-submit").click(function(event){
		$('#password-match-warning').hide()
		$('#password-length-warning').hide()
		if ($('#new-password').val() != $('#new-password-confirm').val()) {
			$('#password-match-warning').show()
			return
		} else {
			$('#password-match-warning').hide()
		}

		if ($('#new-password').val().length < 8) {
			$('#password-length-warning').show()
			return
		} else {
			$('password-length-warning').hide()
		}
	});
})