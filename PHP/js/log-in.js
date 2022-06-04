$(document).ready(function() {
    $("#log-in-form").submit(function(e) {
        const postData = {
            username: $("#username").val(),
            password: $("#password").val()
        };
        $.post("https://www.nekomon.es/ajax/log-in.php", postData, function(response) {
            fetchErrors();
            //$("#log-in-form").trigger("reset");
        });
        e.preventDefault();
    });
});