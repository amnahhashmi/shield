// errand-accept.js
// script for 'accept errand' endpoint

// Keeps track of which page is being viewed.
var pageIndex;

$(document).ready(function() {

	var pages = $(".page")
	pageIndex = 0;

	// custom event for toggling between pages of accept
	$("body").bind("pageEvent", function(e, index){

		// hide all pages
		$(pages).hide()

		// show desired page
		$(pages[index]).show()

		// set pageIndex to reflect shown page 
		pageIndex = index

	})

	// Submit errand accept
	$("#accept-request-button").click(function(event){

		var csrftoken = $('[name=csrfmiddlewaretoken]').val();

		// make POST ajax call
        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            success: function(response){
            	$('body').trigger("pageEvent", pageIndex + 1)
            },
            error: function(jqHXR, exception){
            	console.log(exception);
            }
        })
    })

    $("#livelyhood-home-button").click(function(){
      window.location.pathname = '/';
  	})

	// display last page if errand not open
	if ($("#errand_status").val() != 1) {
		$("body").trigger("pageEvent",2)
	}
	else {
		$("body").trigger("pageEvent",0)
	}
	
});