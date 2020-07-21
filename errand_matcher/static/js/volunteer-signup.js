// volunteer-signup.js
// script for 'volunteer_signup' endpoint

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
      $("#address-input").attr("lat",place.geometry.location.lat())
      $("#address-input").attr("lon",place.geometry.location.lng())
      $("#address-input").attr("zip",zip)
      $("#zipcode-review").text(zip)
  
      $('body').trigger('pageEvent', pageIndex + 1)
    }
  })
}

function validateName() {
  if ($('#firstname-input').val().length > 0 && $('#lastname-input').val().length > 0){
    $("#name-warning").hide();

    // Set review field to user input
    $('#firstname-review').text($('#firstname-input').val());
    $('#lastname-review').text($('#lastname-input').val());
    $('body').trigger("pageEvent", pageIndex + 1);
  }
  else {
     // Show warning
     $("#name-warning").show();
  }
}

function validatePhone() {
  phone = $('#phone-input').val();
  phone = phone.replace(/[^0-9]/g,'');

  $(this).val(
    (phone.slice(0,3) ? "("+phone.slice(0,3)+")" : "") +
    (phone.slice(3,6) ? "-"+phone.slice(3,6) : "") +
    (phone.slice(6,10) ? "-"+phone.slice(6,10) : "")
  );

  if (phone.length==10) {
    $("#phone-warning").hide();
    // Set review field to user input
    $('#phone-review').text(phone);
    $('body').trigger("pageEvent", pageIndex + 1);
  } else {
    $("#phone-warning").show();
  }
}

function validateEmail() {
  var regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;
  if (regex.test($('#email-input').val())) {
    // Set review field to user input
    $("#email-warning").hide()
    $('#email-review').text($("#email-input").val());
    $('body').trigger("pageEvent", pageIndex + 1);
  } else {
    // Show warning and prevent submit
    $("#email-warning").show();
  }
}

$(document).ready(function() {

  var pages = $(".page")
  pageIndex = 0;

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
          $('body').trigger("pageEvent", pageIndex + 1)
        }, 2000)
    }
    else {
      // hide affirmative
      $('.affirmative').css('display','none')
    }
  });

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

  })

  // Progress onBlur or on Enter key pressed
  $('.text-input').bind('blur keyup', function(e) {
    if (e.type === 'blur' || e.keyCode === 13) {
      if (pageIndex == 1) {
        validateName()
      }
      if (pageIndex == 2) {
        validatePhone()
      }
      if (pageIndex == 3) {
        validateEmail()
      }
    }  
  })

  // button behavior
  $(".next-button").click(function(){
    if (pageIndex == 1) {
      validateName()
    }

    if (pageIndex == 2) { 
      validatePhone()
    }

    if (pageIndex == 3) { 
      validateEmail()
    }

    // Set transportation review to user input
    if (pageIndex == 5) {
      var transportations = $.map($("input[name='transport']:checked"), function(item){
        return $(item).val()
      })
      var transportation_as_str = transportations.join(", ")
      $('#transportation-review').text(transportation_as_str)
    }

    // Set frequencyreview to user input
    if (pageIndex == 6) {
      $('#frequency-review').text($("input[name='frequency']:checked").val())
    }

    // Set language review to user input
    if (pageIndex == 7) {
      var languages = $.map($("input[name='languages']:checked"), function(item){
        return $(item).val()
      })
      var languages_as_str = languages.join(", ")
      $('#language-review').text(languages_as_str)
    }

    if (pageIndex == 8) {
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
      window.location.pathname = '/';
    } else {
      $('body').trigger("pageEvent", pageIndex - 1)
    }
  })

  $("#livelyhood-home-button").click(function(){
      window.location.pathname = '/';
  })

  $('#address-input').blur(function(e){
    google.maps.event.trigger(autocomplete, 'place_changed');
  });

  // Submit volunteer form
  $(".finish-set-up").click(function(event){
    event.preventDefault();
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var add_volunteer_url;
    if (location.port) {
       add_volunteer_url = window.location.protocol +'//' + document.domain + ':' + location.port + '/volunteer/signup';
    } else {
      add_volunteer_url = window.location.protocol +'//' + document.domain + '/volunteer/signup';
    }

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
              "language": $("#language-review").text(),
              "lat": $("#address-input").attr("lat"),
              "lon": $("#address-input").attr("lon"),
            },
            success: function(response){
              console.log(response);
            },
            error: function(jqHXR, exception){
              console.log(exception);
            }
        })
        // set welcome field to user name
        $('#welcome-name').text('Welcome to the team, ' + $('#firstname-review').text());
        $('body').trigger("pageEvent", pageIndex + 1)

    })

  // display first page
  $("body").trigger("pageEvent",0)

});