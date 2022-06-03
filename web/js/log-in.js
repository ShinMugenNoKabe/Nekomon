let log_in_form = $('#log-in-form');

log_in_form.submit(function () {
    $("#errors").html("");

    let loginButton = $("#login-button");
    let spinLoadIcon = $("#spin-load-icon");

    // Disable the login button
    loginButton.attr("disabled", true);

    // Show the loading icon
    spinLoadIcon.attr("hidden", false);

    $.ajax({
        type: "post",
        url: "/ajax/login/",
        data: log_in_form.serialize(),
        success: function(data) {
            window.location.href = "/";
        },
        error: function(data) {
            jsonErrors(data);

            // Enable the login button
            loginButton.attr("disabled", false);

            // Stop showing the loading icon
            spinLoadIcon.attr("hidden", true);
        }
    });
    return false;
});