let follow_unfollow_form = $('#follow-unfollow');
let follow_unfollow_button = $('#follow-unfollow-button');
let is_following_input = $('#id_is_following');

follow_unfollow_form.submit(function() {
    $.ajax({
        type: "post",
        url: "/ajax/follow-unfollow/",
        data: follow_unfollow_form.serialize(),
        success: function(data) {
            follow_unfollow_button.html(data.button_text);
            is_following_input.val(data.is_following);

            if (data.is_following == "True") {
                follow_unfollow_button.removeClass("profile-button-green");
                follow_unfollow_button.addClass("profile-button-red");
            } else {
                follow_unfollow_button.removeClass("profile-button-red");
                follow_unfollow_button.addClass("profile-button-green");
            }
        },
        error: function(data) {
            alert("{% trans 'Can\'t do that' %}");
        },
    });
    return false;
});