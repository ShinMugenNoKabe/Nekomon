$(document).ready(function() {
    $("#change-pfp-icon").click(function() {
        $("#id_profile_picture").trigger('click');
    });

    let newProfilePicture = null;

    $("#id_profile_picture").change(function(e) {
        let img = null;
        let cropper = null;

        $("#close-modal").click(function(e) {
            $("#image-cropper").attr("src", null);
            cropper.destroy();
            $("#update-profile-picture-modal").css("display", "none");
        });

        $("#update-profile-picture-modal").css("display", "block");
        $("#image-cropper").attr("src", URL.createObjectURL($("#id_profile_picture").prop("files")[0]));

        img = document.querySelector("#image-cropper");
        cropper = new Cropper(img, {
            aspectRatio: 1 / 1,
                crop() {
                    cropper.getCroppedCanvas().toBlob((blob) => {
                        if (blob != null) {
                            newProfilePicture = new File([blob], "profile_picture.png");
                        }
                    });
            }
        });
    });

    const editProfileButton = $("#edit-profile");
    const editProfileButtonSave = $("#edit-profile-save");
    const editProfileButtonCancel = $("#edit-profile-cancel");

    editProfileButton.click(function() {
        $("#profile-save-button-container").attr("hidden", false);
        $("#profile-cancel-button-container").attr("hidden", false);
        $(editProfileButton).attr("hidden", true);
        $("#update-form-fields").attr("hidden", false);
        $("#profile-info-data").attr("hidden", true);
        $("#messages-update").html("");
    });

    editProfileButtonSave.click(function() {
        $("#id_profile_picture").attr("src", $("#new-profile-picture").attr("src"));

        let fields = $("#update-form-fields");

        let formData = new FormData();

        let name = $(fields).children("input[name='name']").val();
        let username = $(fields).children("input[name='username']").val();
        let description = $(fields).children("textarea[name='description']").val();
        let profile_picture = $(fields).children("input[name='profile_picture']")[0];
        let csrftoken = $(fields).children("input[name='csrfmiddlewaretoken']").val();

        formData.append("name", name);
        formData.append("username", username);
        formData.append("description", description);
        formData.append("profile_picture", newProfilePicture);
        formData.append("csrfmiddlewaretoken", csrftoken);

        $.ajax({
                type: "post",
                enctype: 'multipart/form-data',
                url: "/ajax/update-profile/",
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    // Update user data in the website
                    Array.from($("[data-name='" + data.old_username + "']")).forEach(element => {
                        $(element).text(data.name);
                        $(element).attr("data-name", data.new_username);
                    });

                    if (data.new_username) {
                        
                    }

                    Array.from($("[data-username-link='" + data.old_username + "']")).forEach(element => {
                        $(element).attr("href", "/" + data.new_username);
                        $(element).attr("data-username-link", data.new_username);
                    });

                    Array.from($("[data-pfp='" + data.old_username + "']")).forEach(element => {
                        $(element).attr("src", "https://i.imgur.com/" + data.profile_picture + ".png");
                        $(element).attr("data-pfp", data.new_username);
                    });

                    $("[data-description='" + data.old_username + "']").text(data.description);

                    Array.from($("[data-username='" + data.old_username + "']")).forEach(element => {
                        $(element).text("@" + data.new_username);
                        $(element).attr("data-username", data.new_username);
                    });

                    resetProfileInfo();
                },
                error: function(data) {
                    console.log(data);
                    $("#messages-update").html("<div class='flash-message'>" + data.responseJSON.error + "</div>");
                },
            });
    });

    function resetProfileInfo() {
        $("#profile-save-button-container").attr("hidden", true);
        $("#profile-cancel-button-container").attr("hidden", true);
        $(editProfileButton).attr("hidden", false);
        $("#update-form-fields").attr("hidden", true);
        $("#profile-info-data").attr("hidden", false);

        $("#image-cropper").attr("src", null);
        cropper.destroy();
        newProfilePicture = null;
    }

    editProfileButtonCancel.click(resetProfileInfo);
});