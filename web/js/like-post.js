let follow_unfollow_form = $('#follow-unfollow');

follow_unfollow_form.submit(function() {
    $.ajax({
        type: "post",
        url: "/ajax/follow-unfollow/",
        data: follow_unfollow_form.serialize(),
        success: function(data) {
            if (data == "true") {

            } else {

            }
        },
        /*error: function(data) {
            $("#errors").html("<div class='flash-message'>" + data.responseJSON.error + "</div>");
        }*/
    });
    return false;
});