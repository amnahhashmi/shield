// complete-signup.js
// script for 'complete_signup' endpoint

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

// var autocomplete;

// // Initialize the Google Maps API autocomplete widget for address entry.
function initAutocomplete() {
  // Create the autocomplete object, restricting the search predictions to
  // geographical location types.

  autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('address-input'), {types: ['geocode']});

  // Avoid paying for data that you don't need by restricting the set of
  // place fields that are returned to just the address components.
  autocomplete.setFields(['address_component','geometry']);

  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
  autocomplete.addListener('place_changed', function(){
  	// Populate confirmation page and POST form
  });
}

$(document).ready(function() {

	var pages = $(".page")
	var pageIndex = 0;

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
		
		// Set transportation review to user input
		if (pageIndex == 2) {
			var transportation = [];
			if ($("#transport-feet-cbox").is(":checked")){
				transportation.push("My own two feet");
			}
			if($("#transport-bike-cbox").is(":checked")){
				transportation.push("Bike");
			}
			if($("#transport-car-cbox").is(":checked")){
				transportation.push("Car");
			}

			var transportation_as_str = transportation.join(", ")
			$('#transportation-review').text(transportation_as_str)
		}

		// Set frequencyreview to user input
		if (pageIndex == 3) {
			var frequency = [];
			if ($("#freq-anytime-cbox").is(":checked")){
				frequency.push("Anytime");
			}
			if($("#freq-multi-week-cbox").is(":checked")){
				frequency.push("2-3 times a week");
			}
			if($("#freq-once-week-cbox").is(":checked")){
				frequency.push("Once a week");
			}

			// Can only have one option selected
			if (frequency.length > 1) {
				$("#frequency-warning").show()
				return;
			}
			else {
				var frequency_as_str = frequency.join(", ")
			$('#frequency-review').text(frequency_as_str)
			
			}
		}

		// Set language review to user input
		if (pageIndex == 4) {
			var languages = [];
			if($("#spanish-cbox").is(":checked")){
				languages.push("Spanish");
			}
			if($("#russian-cbox").is(":checked")){
				languages.push("Russian");
			}
			if($("#chinese-cbox").is(":checked")){
				languages.push("Chinese");
			}

			var languages_as_str = languages.join(", ")
			$('#language-review').text(languages_as_str)
		}

		// Validate user certified health and safety protocl
		if (pageIndex == 5) {
			if (!$("#certify-health-safety-protocol-cbox").is(":checked")) {
				$("#health-safety-warning").show()
				return;
			}
		}

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
			$('#firstname-review').text($('#firstname-input').val());
			$('#lastname-review').text($('#lastname-input').val());
			$('body').trigger("pageEvent", pageIndex + 1);
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

	// Submit volunteer form
	$(".finish-set-up").click(function(event){
		event.preventDefault();
		var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
		var add_volunteer_url = window.location.protocol +'//' + document.domain + ':8000/volunteer';
		// make POST ajax call
        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            url: add_volunteer_url,
            data: {
            	"first_name": $("#firstname-review").text(),
            	"last_name": $("#lastname-review").text(),
            	"email": $("#email-review").text(),
            	"mobile_number": $("#phone-review").text(),
            	"frequency": $("#frequency-review").text(),
            	"transportation": $("#transportation-review").text(),
            	"language": $("#language-review").text()
            },
            success: function(response){
            	console.log(response);
            },
            error: function(jqHXR, exception){
            	console.log(exception);
            }
        })
        $('body').trigger("pageEvent", pageIndex + 1)

    })

	// display first page
	$("body").trigger("pageEvent",0)

});