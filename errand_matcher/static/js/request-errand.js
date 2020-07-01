// request-errand.js
// script for 'request-errand' endpoint

$(document).ready(function() {
	var pages = $(".page")
	pageIndex = 0;

	// custom event for toggling between pages of errand form
	$("body").bind("pageEvent", function(e, index){

		// hide all pages
		$(pages).hide()

		// show desired page
		$(pages[index]).show()

		// set pageIndex to reflect shown page 
		pageIndex = index

	})

	// button behavior

	$(".back-button").click(function(){
		window.location.replace(window.location.origin + "/home");
	})


	$(".next-button").click(function(){
		$('body').trigger("pageEvent", pageIndex + 1)
	})

	$(".health-and-safety-button").click(function(){
		window.location.replace(window.location.origin + "/health");
	})

	$(".faq-button").click(function(){
		window.location.replace(window.location.origin + "home#above-faq");
	})

	$(".support-button").click(function(){
		window.location.replace(window.location.origin + "home#above-about");
	})

	// display first page
	$("body").trigger("pageEvent",0)

	// Submit errand
	$("#delivery-request-button").click(function(event){

		var csrftoken = $('[name=csrfmiddlewaretoken]').val();

		// make POST ajax call
        $.ajax({
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            url: "/errand",
            data: {
            	"requestor_number": $("#requestor-number").val(),
            	"urgency": $("input[name='errand-urgency']:checked").val(),
            	"additional_info": $("#errand-additional-info").val()
            },
            success: function(response){
            	console.log(response)
            },
            error: function(jqHXR, exception){
            	console.log(exception);
            }
        })

        $('body').trigger("pageEvent", pageIndex + 1)
    })


});
