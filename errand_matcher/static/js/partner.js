// partner.js
// script for 'partner' endpoint

// Google Maps autocomplete widget
var autocomplete;

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      var circle = new google.maps.Circle(
          {center: geolocation, radius: position.coords.accuracy});
      autocomplete.setBounds(circle.getBounds());
    });
  }
}

// // Initialize the Google Maps API autocomplete widget for address entry.
function initAutocomplete() {
  // Create the autocomplete object, restricting the search predictions to
  // geographical location types.

  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('add-requestor-address'), {types: ['geocode']});

  // Avoid paying for data that you don't need by restricting the set of
  // place fields that are returned to just the address components.
  autocomplete.setFields(['address_component','geometry']);

  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
  autocomplete.addListener('place_changed', function(){

    var place = autocomplete.getPlace();
    var zip;

    $.each(place ? place.address_components : [], function(){
      if (this.types[0] == "postal_code") {
        zip = this.long_name;
      }
    });


    // SV Question: What should we do if address is provided with no ZIP code (but valid lat/lng)?
    if (!place || !place.geometry || !place.address_components || !zip) {
      // User entered the name of a Place that was not suggested and
      // pressed the Enter key, or the Place Details request failed.
      $("#address-warning").show();
      return;
    } else {
      $("#add-requestor-address").attr("lat",place.geometry.location.lat())
      $("#add-requestor-address").attr("lon",place.geometry.location.lng())
      $("#add-requestor-address").attr("zip",zip)
    }
  })
}

$(document).ready(function() {
	// add delivery button modal behavior
	$("#add-delivery-button").click(function(){
		$("#add-delivery-modal").show()

    });

    $("#cancel-delivery-button").click(function(){
    	$("#add-delivery-form")[0].reset()
		$("#add-delivery-modal").hide()

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

	// display text on request status
	$(".errand-status-icon").hover(
		function() {
			var displayTextID = "#errand_status_text_" + this.id.slice(-1);
			$(displayTextID).show()
		}, function() {
			var displayTextID = "#errand_status_text" + this.id.slice(-1);
			$(".hover_8").hide()
		}
	);

	// edit delivery button modal behavior
	$(".edit-delivery-button").click(function(){
		var idParts = this.id.split('_');
		var errandID = idParts.pop();
		var requestorID = idParts.pop();
		var dueByDate = new Date($("#due_by_" + requestorID + "_" + errandID).text());
		var dueByDateDay = ("0" + dueByDate.getDate()).slice(-2);
		var dueByDateMonth = ("0" + (dueByDate.getMonth() + 1)).slice(-2);

		$("#edit-requestor-phone").val($("#mobile_number_" + requestorID + "_" + errandID).text())
		$("#edit-requestor-first-name").val($("#first_name_" + requestorID + "_" + errandID).text())
		$("#edit-requestor-last-name").val($("#last_name_" + requestorID + "_" + errandID).text())
		$("#edit-requestor-address").val($("#address_str_" + requestorID + "_" + errandID).text())
		$("#edit-requestor-apartment").val($("#apt_no_" + requestorID + "_" + errandID).text())
		$("#edit-errand-due-by").val(dueByDate.getFullYear() + "-" + dueByDateMonth + "-" + dueByDateDay)
		$("#edit-volunteer-instructions").val($("#additional_info_" + requestorID + "_" + errandID).text())
		$("#edit-internal-notes").val($("#internal_note_" + requestorID + "_" + errandID).text())
		$("#edit-requestor-id").val(requestorID)
		$("#edit-errand-id").val(errandID)
		$("#edit-delivery-modal").show()

    });

    $("#cancel-changes-button").click(function(){
    	$("#edit-delivery-form")[0].reset()
		$("#edit-delivery-modal").hide()
    });


    // delete delivery button inside edit modal behavior
	$("#cancel-existing-delivery-button").click(function(event){
		event.preventDefault();
		var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		var delete_errand_url;
		if (location.port) {
			 delete_errand_url = window.location.protocol +'//' + document.domain + ':' + location.port + '/partner/request/delete/' + $("#edit-errand-id").val();
		} else {
			delete_errand_url = window.location.protocol +'//' + document.domain + '/partner/request/delete/' + $("#edit-errand-id").val();
		}

		// make DELETE ajax call
        $.ajax({
            type: 'DELETE',
            headers: {'X-CSRFToken': csrftoken},
            url: delete_errand_url,
            success: function(response){
            	location.reload();
            },
            error: function(jqHXR, exception){
            	console.log(exception);
            }
        })
    });

    // delete delivery button inside table behavior
	$(".cancel-delivery-button").click(function(event){
		event.preventDefault();
		var idParts = this.id.split('_');
		var errandID = idParts.pop();
		var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		var delete_errand_url;
		if (location.port) {
			 delete_errand_url = window.location.protocol +'//' + document.domain + ':' + location.port + '/partner/request/delete/' + errandID;
		} else {
			delete_errand_url = window.location.protocol +'//' + document.domain + '/partner/request/delete/' + errandID;
		}
		
		// make DELETE ajax call
        $.ajax({
            type: 'DELETE',
            headers: {'X-CSRFToken': csrftoken},
            url: delete_errand_url,
            success: function(response){
            	location.reload();
            },
            error: function(jqHXR, exception){
            	console.log(exception);
            }
        })
    });

	// navbar button behavior
	var home_url;
	if (location.port) {
		home_url = window.location.protocol +'//' + document.domain + ':' + location.port;
	} else {
		home_url = window.location.protocol +'//' + document.domain;
	}
	
    
	$('#home-item').click(function(){
		window.location.href = home_url;
	})

	$('.health-and-safety-link').click(function(){
		window.location.href = home_url + "/health";
	})

	$('.faq-link').click(function(){
		window.location.href = home_url + "#above-faq"
	})

	$('.about-link').click(function(){
		window.location.href = home_url +"#above-about";
	})

	$('#user-menu-button').click(function(){
		$('#user-sidebar').show()
	})

	$('#close-user-menu').click(function(){
		$('#user-sidebar').hide()
	})
})