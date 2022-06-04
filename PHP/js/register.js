$(document).ready(function() {
    $("#register-form").submit(function(e) {
        const postData = {
            email: $("#email").val(),
            username: $("#username").val(),
            password: $("#password").val(),
            password2: $("#password2").val()
        };
        $.post("https://www.nekomon.es/ajax/register.php", postData, function (response) {
            fetchErrors();
            //$("#register-form").trigger("reset");
        });
        e.preventDefault();
    });
});