// partner.js
// script for 'partner' endpoint

$(document).ready(function() {
	// add delivery button modal behavior
	$("#add-delivery-button").click(function(){
		$("#add-delivery-modal").show()

    });

    $("#cancel-delivery-button").click(function(){
    	$("#add-delivery-form")[0].reset()
		$("#add-delivery-modal").hide()

    });

	// Date Object
	var minDateStr;
	var nowHour = new Date().getHours();
	if (nowHour <= 17) {
		minDateStr = '+1d'
	}
	else {
		minDateStr = '+2d'
	}

	$('#datepicker').datepicker({
		minDate: minDateStr, 
		maxDate: '+1m',
		defaultDate: '+5d'
	});

	// submit delivery error checking
	$("#add-delivery-submit").click(function(e){
		// validate phone input
		phone = $('#add-requestor-phone').val();
		phone = phone.replace(/[^0-9]/g,'');

		$('#add-requestor-phone').val(
			(phone.slice(0,3) ? "("+phone.slice(0,3)+")" : "") +
			(phone.slice(3,6) ? "-"+phone.slice(3,6) : "") +
			(phone.slice(6,10) ? "-"+phone.slice(6,10) : "")
		);

		if (phone.length==10) {
			$("#phone-warning").hide();
		} else {
			e.preventDefault()
			$("#phone-warning").show().focus();
			return
		}
	});
})