// complete-signup.js
// script for 'request' endpoint

// Keeps track of which page is being viewed.
var pageIndex;

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

function distance(lat1, lon1, lat2, lon2) {
	if ((lat1 == lat2) && (lon1 == lon2)) {
		return 0;
	}
	else {
		var radlat1 = Math.PI * lat1/180;
		var radlat2 = Math.PI * lat2/180;
		var theta = lon1-lon2;
		var radtheta = Math.PI * theta/180;
		var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
		if (dist > 1) {
			dist = 1;
		}
		dist = Math.acos(dist);
		dist = dist * 180/Math.PI;
		dist = dist * 60 * 1.1515;
		return dist;
	}
}

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

		var place = autocomplete.getPlace();
		var address = {};

		$.each(place ? place.address_components : [], function(){
			var property = {}
			property[this.types[0]] = this.short_name;
			$.extend(address, property)
		});

		// SV Question: What should we do if address is provided with no ZIP code (but valid lat/lng)?
		if (!place || !place.geometry || !address['postal_code']) {
			// User entered the name of a Place that was not suggested and
	    	// pressed the Enter key, or the Place Details request failed.
			$("#address-warning").show();
			return;
		} else {
			lat = place.geometry.location.lat()
			lng = place.geometry.location.lng()
			
			// User entered address outside of range from target (HBS)
			target_lat = 42.36722
			target_lng = -71.12253
			dist = distance(lat, lng, target_lat, target_lng);
			if (dist > 10) {
				$("#address-warning").hide()
				$("#outside-of-boston-warning").show();
				return;
			}
			else {
				$("#address-input").attr("lat",lat)
				$("#address-input").attr("lon",lng)
				$("#address-review").val($("#address-input").val());
				$('body').trigger('pageEvent', pageIndex + 1)
			}

		}
	});

	// This prevents chrome's address autocomplete feature from interfering with the maps widget.
	var observer = new MutationObserver(function() {
        observer.disconnect();
        $("#address-input").attr("autocomplete", "chrome-off");
    });

    observer.observe($("#address-input").get(0), {
        attributes: true,
        attributeFilter: ['autocomplete']
    });

}

$(document).ready(function() {

	var pages = $(".page")
	pageIndex = 0;

	// custom event for toggling between pages of signup form
	$("body").bind("pageEvent", function(e, index){

		// hide all pages
		$(pages).hide()

		// show desired page
		$(pages[index]).show()

		// set pageIndex to reflect shown page 
		pageIndex = index

		// update progress bar
		progressBarLocation = (2 + pageIndex)/ pages.length

		$("stop").slice(1,3).attr("offset",progressBarLocation)

	})

	// 
	$("body").bind("partialSubmitEvent", function(e) {

		switch(pageIndex) {

			// requirements checkbox validation
			// requestor must meet at least one requirement
			case 0:
				if ($('.req-input:checked').length == 0) {
					$('#requirements-warning').show().focus()
					return;
				} else {
					break;
				}

			// name input validation
			// requestor must enter something for both first and last name
			case 1:
				if ($('#firstname-input').val().length == 0 || $('#lastname-input').val().length == 0){
					$('#name-warning').show().focus()
					return;
				} else {
					$('#firstname-review').val($('#firstname-input').val());
					$('#lastname-review').val($('#lastname-input').val());
					break;
				}

			// date of birth validation
			// must input a complete, valid date which is in the past
			case 2:
				date_input = moment($('#dob-input').val(),"YYYY-MM-DD")
				if(!date_input.isValid() || !date_input.isBefore()){
					// $("#dob-warning").show().focus()
					return;
					// TODO: further validation to accord with 65+ restriction? 
				} else {
					break;
				}

			case 3:
				if ($("input[name='contact']:checked").length == 0) {
					return;
				} else {
					$("#contact-review").val($("input[name='contact']:checked").val())
					break;
				}

			case 4:
				// validate date
		        date_input = moment($('#dob-input').val(),"YYYY-MM-DD")
		        if(!date_input.isValid() || !date_input.isBefore()){
		            $("#dob-warning").show().focus()
		            return;
		        } else {
		            $("#dob-warning").hide()
		            // Set review field to user input
					$('#dob-review').val($("#dob-input").val());
					break;
		        }

			case 5:
				phone = $("#phone-input").val();
				phone = phone.replace(/[^0-9]/g,'');

				$("#phone-input").val(
					(phone.slice(0,3) ? "("+phone.slice(0,3)+")" : "") +
					(phone.slice(3,6) ? "-"+phone.slice(3,6) : "") +
					(phone.slice(6,10) ? "-"+phone.slice(6,10) : "")
				);

				if (phone.length!=10) {
					$("#phone-warning").show();
					return;
				} else {
					// Set review field to user input
					$('#phone-review').val($("#phone-input").val());
					break;
				}
		}

		$('body').trigger("pageEvent", pageIndex + 1)
	})

	// button behavior
	$(".next-button").click(function(){
		$('body').trigger("partialSubmitEvent")
	})


	$(".back-button").click(function(){
		if (pageIndex == 0) {
			// send to landing page
			window.location.pathname = '/';
		} else {
			$('body').trigger("pageEvent", pageIndex - 1)
		}
	})

	$("#redo-button").click(function(){
		window.location.pathname = "/requestor";
	});

	// If all name input fields are full on blur/defocus, automatically progress
	$('#firstname-input, #lastname-input').blur(function(e){
		if ($('#firstname-input').val().length > 0 && $('#lastname-input').val().length > 0){
			$('body').trigger("partialSubmitEvent");
		}
	});

	// single input blur with nonempty input -> progress form
	$('#phone-input, #dob-input').blur(function(e){
		if($(e.target).val().length > 0) {
			$('body').trigger("partialSubmitEvent")
		}
	});

	$('#address-input').blur(function(e){
		google.maps.event.trigger(autocomplete, 'place_changed');
	});

    $('.icon').click(function(){
        var topnav = document.getElementById("topnav");
        if (topnav.className === "topnav") {
          topnav.className += " responsive";
        } else {
          topnav.className = "topnav";
        }
        $(topnav).next().css("margin-top",topnav.scrollHeight);
    });

	$('.top-link').click(function(){
		window.location.href ="/#top";
	})

	$('.health-and-safety-link').click(function(){
		window.location.href = "/health";
	})

	$('.faq-link').click(function(){
		window.location.href = "/#above-faq";
	})

	$('.about-link').click(function(){
		window.location.href = "/#above-about";
	})

	function collapseTopNav() {
		var topnav = document.getElementById("topnav");
        if (topnav.className === "topnav") {
          return;
        } else {
          topnav.className = "topnav";
        }
	}

	$('#request-button').click(function(){
		window.location.href = "/errand";
	})

	$('#faq-button').click(function(){
		window.location.href = "/#above-faq";
	})

	$('#support-button').click(function(){
		// SV 4/11/20 : Should be a link to support page once that exists
		window.location.href = "/#above-about";
	})

	// display first page
	$("body").trigger("pageEvent",0)
}); 
