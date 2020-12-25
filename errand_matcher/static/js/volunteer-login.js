$(document).ready(function() {
    $('#volunteer-login-button').click(function(e){
        // validate phone

      phone = $('#volunteer-login-phone').val();
      phone = phone.replace(/[^0-9]/g,'');

      if (phone.length==10) {
        $("#phone-warning").hide();
      } else {
        e.preventDefault()
        $("#phone-warning").show();
        $("#phone-warning").focus();
      }
    })

    $('#volunteer-login-otp-button').click(function(e){
        // validate 6-digit code

        otp = $('#volunteer-login-otp').val()

        otp = otp.replace(/[^0-9]/g,'');
        if (otp.length==6) {
            $("#otp-warning").hide();
          } else {
            e.preventDefault()
            $("#otp-warning").show();
            $("#otp-warning").focus();
          } 
    })
});