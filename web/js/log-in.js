let log_in_form = $('#log-in-form');

log_in_form.submit(function () {
    $.ajax({
        type: "post",
        url: "/ajax/login/",
        data: log_in_form.serialize(),
        success: function(data) {
            window.location.href = "/";
        },
        error: function(data) {
            jsonErrors(data);
        }
    });
    return false;
});