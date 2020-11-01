// volunteer-signup.js
// script for 'volunteer_signup' endpoint


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
    document.getElementById('add-volunteer-address'), {types: ['geocode']});

  // Avoid paying for data that you don't need by restricting the set of
  // place fields that are returned to just the address components.
  autocomplete.setFields(['address_component','geometry']);

  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
  autocomplete.addListener('place_changed', function(){

    const place = autocomplete.getPlace();
    if (!place || !place.geometry || !place.address_components ) {
      $("#address-warning").show();
    } else {
      $("#address-warning").hide();
      $("#address-latitude").val(place.geometry.location.lat())
      $("#address-longitude").val(place.geometry.location.lng())
    }
  });

  // This prevents chrome's address autocomplete feature from interfering with the maps widget.
  var observer = new MutationObserver(function() {
      observer.disconnect();
      $("#add-volunteer-address").attr("autocomplete", "chrome-off");
  });

  observer.observe($("#add-volunteer-address").get(0), {
      attributes: true,
      attributeFilter: ['autocomplete']
  });
}

function validateAddress(e) {
  address = $("#add-volunteer-address").val()
  if (address.length == 0 || $("#address-warning").is(':visible')){
    e.preventDefault()
    $("#address-warning").show();
    $("#address-warning").focus();
  }
}

function validateFirstName(e) {
  first_name = $('#add-volunteer-first-name').val();
  if (first_name.length == 0) {
    e.preventDefault()
    $("#first-name-warning").show();
    $("#first-name-warning").focus();
  } else {
    first_name_trimmed = first_name.trim();
    if (first_name_trimmed.length > 0) {
      $("#first-name-warning").hide()
      $('#add-volunteer-first-name').val(first_name_trimmed)
    } else {
      e.preventDefault()
      $("#first-name-warning").show();
      $("#first-name-warning").focus();
    }
  }
}

function validateLastName(e) {
  last_name = $('#add-volunteer-last-name').val();
  if (last_name.length == 0) {
    e.preventDefault()
    $("#last-name-warning").show();
    $("#last-name-warning").focus();
  } else {
    last_name_trimmed = last_name.trim();
    if (last_name_trimmed.length > 0) {
      $("#last-name-warning").hide()
      $('#add-volunteer-last-name').val(last_name_trimmed)
    } else {
      e.preventDefault()
      $("#last-name-warning").show();
      $("#last-name-warning").focus();
    }
  }
}

function validatePhone(e) {
  phone = $('#add-volunteer-phone').val();
  phone = phone.replace(/[^0-9]/g,'');

  $(this).val(
    (phone.slice(0,3) ? "("+phone.slice(0,3)+")" : "") +
    (phone.slice(3,6) ? "-"+phone.slice(3,6) : "") +
    (phone.slice(6,10) ? "-"+phone.slice(6,10) : "")
  );

  if (phone.length==10) {
    $("#phone-warning").hide();
  } else {
    e.preventDefault()
    $("#phone-warning").show();
    $("#phone-warning").focus();
  }
}

function validateEmail(e) {
  email = $('#add-volunteer-email').val();
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    $("#email-warning").hide();
  } else {
    e.preventDefault()
    $("#email-warning").show();
    $("#email-warning").focus();
  } 
}

function validateTransport(e) {
  if ($('.transport-check:checked').length > 0) {
    $("#transport-warning").hide()
    var transportations = $.map($("input[name='transport']:checked"), function(item){
        return $(item).val()
      })
    var transportation_as_str = transportations.join(", ")
    $('#transportationChecked').val(transportation_as_str)
  } else {
    e.preventDefault()
    $("#transport-warning").show()
    return
  }
}

function validateLanguage(e) {
  if ($('.language-check:checked').length > 0) {
    $("#language-warning").hide()
    var languages = $.map($("input[name='language']:checked"), function(item){
        return $(item).val()
      })
    var language_as_str = languages.join(", ")
    $('#languageChecked').val(language_as_str)
  } else {
    e.preventDefault()
    $("#language-warning").show()
    return
  }
}

function validateFrequency(e) {
  if ($('.frequency-check:checked').length > 0) {
    $("#frequency-warning").hide()
  } else {
    e.preventDefault()
    $("#frequency-warning").show()
    return
  }
}

function validateEligibility(e) {
  if ($('.eligibility-check:checked').length == $('.eligibility-check').length) {
    $("#eligibility-warning").hide()
  } else {
    e.preventDefault()
    $("#eligibility-warning").show()
    return
  }
}

function validateHealthSafety(e) {
  if ($('#volunteerHealthSafetyCheck1').is(":checked")) {
    $("#health-safety-warning").hide()
  } else {
    e.preventDefault()
    $("#health-safety-warning").show()
    return
  }
}

function validateAcknowledgment(e) {
  if ($('#volunteerAcknowledgmentCheck1').is(":checked")) {
    $("#acknowledgment-warning").hide()
  } else {
    e.preventDefault()
    $("#acknowledgment-warning").show()
    return
  }
}

$(document).ready(function() {
  $('#add-volunteer-address').blur(function(e){
    google.maps.event.trigger(autocomplete, 'place_changed');
  });

  $("#add-volunteer-submit").click(function(e){
    validateFirstName(e);
    validateLastName(e);
    validatePhone(e);
    validateEmail(e);
    validateAddress(e);
    validateTransport(e);
    validateLanguage(e);
    validateFrequency(e);
    validateEligibility(e);
    validateHealthSafety(e);
    validateAcknowledgment(e);
  });

  $("#add-volunteer-first-name").change(function(e){
    validateFirstName(e);
  });

  $("#add-volunteer-last-name").change(function(e){
    validateLastName(e);
  });

  $("#add-volunteer-phone").change(function(e){
    validatePhone(e);
  });

  $("#add-volunteer-email").change(function(e){
    validateEmail(e);
  });

  $(".transport-check").change(function(e){
    validateTransport(e);
  });

  $(".language-check").change(function(e){
    validateLanguage(e);
  });

  $(".frequency-check").change(function(e){
    validateFrequency(e);
  });

  $(".eligibility-check").change(function(e){
    validateEligibility(e);
  });

  $('#volunteerHealthSafetyCheck1').change(function(e){
    validateHealthSafety(e);
  });

  $("#volunteerAcknowledgmentCheck1").change(function(e){
    validateAcknowledgment(e);
  });

  $("#livelyhood-home-button").click(function(){
      window.location.pathname = '/';
  })
})