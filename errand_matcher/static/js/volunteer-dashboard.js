// volunteer-dashboard.js
// script for 'volunteer_dashboard' endpoint

$(document).ready(function() {

  // edit profile button modal behavior
  $("#edit-profile-button").click(function(){
    $("#edit-profile-modal").show()
    });

  $("#cancel-edit-profile-button").click(function(){
    $("#edit-profile-modal").hide()
    });

  $('#user-menu-button').click(function(){
    $('#user-sidebar').show()
  })

  $('#close-user-menu').click(function(){
    $('#user-sidebar').hide()
  })
})