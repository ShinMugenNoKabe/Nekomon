let register_form = $('#register-form');

register_form.submit(function () {
    $("#errors").html("");

    let registerButton = $("#login-button");
    let spinLoadIcon = $("#spin-load-icon");

    // Disable the register button
    registerButton.attr("disabled", true);

    // Show the loading icon
    spinLoadIcon.attr("hidden", false);

    $.ajax({
        type: "post",
        url: "/ajax/new-account/",
        data: register_form.serialize(),
        success: function(data) {
            window.location.href = "/";
        },
        error: function(data) {
            jsonErrors(data);

            // Enable the register button
            registerButton.attr("disabled", false);

            // Stop showing the loading icon
            spinLoadIcon.attr("hidden", true);
        }
    });
    return false;
});