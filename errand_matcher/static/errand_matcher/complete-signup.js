// complete-signup.js
// script for 'begin_signup' endpoint

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

		// populate confirmation fields
		$("#name-confirmation").text($("#firstname-input").val()+" "+$("#lastname-input").val())

		// todo: learnhow to retrieve email
		$("#email-confirmation").text("NEED EMAIL FROM CONF-TOKEN")

		$("#phone-confirmation").text($('#phone-input').val())

		$("transport-confirmation").text($)

		// todo handle button activation/deactivation
	})

	// button behavior
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

	// If all name input fields are full on blur/defocus, automatically progress
	$('#name-page').find(".text-input").blur(function(e){
		if ($('#firstname-input').val().length > 0 && $('#lastname-input').val().length > 0){
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
			$('body').trigger("pageEvent", pageIndex + 1)
		} else {
			// todo: display a warning message
		}
	})

	$('#address-input').blur(function(e){
		// todo: validate
		$('body').trigger("pageEvent", pageIndex + 1)
	})

	// display first page
	$("body").trigger("pageEvent",0)

});