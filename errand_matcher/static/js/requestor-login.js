$(document).ready(function() {
    $('#requestor-login-button').click(function(e){
        // validate date
        date_input = moment($('#dob-input').val(),"YYYY-MM-DD")
        if(!date_input.isValid() || !date_input.isBefore()){
            e.preventDefault()
            $("#dob-warning").show().focus()
            return;
        } else {
            $("#dob-warning").hide()
        }

        // validate phone
        phone = $("#phone-input").val();
        phone = phone.replace(/[^0-9]/g,'');

        $("#phone-input").val(
            (phone.slice(0,3) ? "("+phone.slice(0,3)+")" : "") +
            (phone.slice(3,6) ? "-"+phone.slice(3,6) : "") +
            (phone.slice(6,10) ? "-"+phone.slice(6,10) : "")
        );

        if (phone.length!=10) {
            e.preventDefault()
            $("#phone-warning").show().focus();
            return;
        } else {
          $("#phone-warning").hide();  
        }     
    })
});


