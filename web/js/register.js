let register_form = $('#register-form');

register_form.submit(function () {
    $.ajax({
        type: "post",
        url: "/ajax/new-account/",
        data: register_form.serialize(),
        success: function(data) {
            window.location.href = "/";
        },
        error: function(data) {
            jsonErrors(data);
        }
    });
    return false;
});