$(document).ready(function() {
    const editProfileButton = $("#edit-profile");

    editProfileButton.click(function() {
        const name = $("#user-name");
        name.html("<input type='text'>");

        const username = $("#user-username");
        username.html("<input type='text'>");

        const description = $("#user-description");
        description.html("<input type='text'>");

        const csrftoken = $("#profile-header").children('input[name="csrfmiddlewaretoken"]').val();

        editProfileButton.text("Guardar");

        editProfileButton.click(function() {
            $.ajax({
                type: "post",
                url: "/ajax/update-profile/",
                data: {
                    "name": name.val(),
                    "username": username.val(),
                    "description": description.val(),
                    "csrftoken": csrftoken
                },
                success: function(data) {
                    /*if (data == "True") {
                        follow_unfollow_button.html("Dejar de seguir");
                        is_following_input.val(data);
                    } else {
                        follow_unfollow_button.html("Seguir");
                        is_following_input.val(data);
                    }*/
                },
                error: function(data) {
                    console.log("An error has ocurred");
                },
            });
        });
    });
});