$(document).ready(function() {
    const editProfileButton = $("#edit-profile");
    const editProfileButtonSave = $("#edit-profile-save");

    editProfileButton.click(function() {
        $("#profile-save-button-container").attr("hidden", false);
        $(editProfileButton).attr("hidden", true);
        $("#update-form-fields").attr("hidden", false);
        $("#profile-info-data").attr("hidden", true);
    });

    editProfileButtonSave.click(function() {
        $.ajax({
                type: "post",
                url: "/ajax/update-profile/",
                data: $("#update-form").serialize(),
                success: function(data) {
                    // Update user data in the website
                    Array.from($('[data-username]')).forEach(element => {
                        $(element).text("@" + data.username);
                    });

                    Array.from($('[data-name]')).forEach(element => {
                        $(element).text(data.name);
                    });

                    Array.from($('[data-username-link]')).forEach(element => {
                        $(element).attr("href", "/" + data.username);
                    });

                    $("#profile-save-button-container").attr("hidden", true);
                    $(editProfileButton).attr("hidden", false);
                    $("#update-form-fields").attr("hidden", true);
                    $("#profile-info-data").attr("hidden", false);
                },
                error: function(data) {
                    $("#errors-update").html("<div class='flash-message'>" + data.responseJSON.error + "</div>");
                },
            });
    });
});