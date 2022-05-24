let post_box = $('#upload-post');
let image = $(post_box).children("input[name='image']")[0];
let imagePreviewContainer = $("#image-preview-container");

$(image).change(function(e) {
    let imagePreview = $("#image-preview");

    // Create blob image
    $(imagePreview).attr("src", URL.createObjectURL(e.target.files[0]));

    // Show the preview
    $(imagePreviewContainer).css("display", "block");
});

function removeImage() {
    // Stop showing the preview
    $(imagePreviewContainer).css("display", "none");

    // Remove the image
    $(image).val(null);
}

$("#remove-image-button").click(removeImage);

if (typeof postSocket !== "undefined") {
    postSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        // Update posts
        $("#posts").html(data.new_post + $("#posts").html());

        // Update timeago
        $("time.timeago").timeago();
    };

    postSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
}

if (typeof postViewSocket !== "undefined") {
    postViewSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        // Update posts
        $("#replies").html($("#replies").html() + data.new_post);

        // Update timeago
        $("time.timeago").timeago();
    };

    postViewSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
}

post_box.submit(function (e) {
    let uploadButton = $("#new-post-button");
    let spinLoadIcon = $("#spin-load-icon");

    $("#errors").html("");

    // Disable the upload button
    uploadButton.attr("disabled", true);

    // Show the loading icon
    spinLoadIcon.attr("hidden", false);

    let formData = new FormData();

    let content = $(post_box).children("textarea[name='content']").val();
    let image = $(post_box).children("input[name='image']")[0];
    let in_response_to = $(post_box).children("input[name='in_response_to']").val();
    //let in_response_to = 1;
    let csrftoken = $(post_box).children("input[name='csrfmiddlewaretoken']").val();

    formData.append("content", content);
    formData.append("image", image.files[0]);
    formData.append("in_response_to", in_response_to);
    formData.append("csrfmiddlewaretoken", csrftoken);

    $.ajax({
        type: "post",
        enctype: 'multipart/form-data',
        url: "/ajax/new-post/",
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            $('#id_content').val("");
            $("#char-count").html("");

            const socket = typeof postSocket !== "undefined" ? postSocket : postViewSocket;

            socket.send(JSON.stringify({
                'post': data.post
            }));

            console.log(socket.readyState);

        },
        error: function(data) {
            $("#errors").html("<div class='flash-message'>" + data.responseJSON.error + "</div>");
        },
        complete: function() {
            // Remove the image once its uploaded
            removeImage();

            // Enable the upload button
            uploadButton.attr("disabled", false);

            // Stop showing the loading icon
            spinLoadIcon.attr("hidden", true);
        }
    });
    return false;
});

$(document).ready(function() {
    $("#select-image-icon").click(function() {
        $("#id_image").trigger('click');
    });

    /*$("#id_content").keypress(function(e) {
        let keycode = (e.keyCode ? e.keyCode : e.which);

        if (keycode == "13") {
            $("#upload-post").submit();
            $("#id_content").html("test");
        };
    });*/

    $("#id_content").on("keydown keyup", function(e) {
        $("#char-count").html(140 - this.value.length);
        let numero = $("#char-count").html();

        if (numero <= 140 && numero >= 80) {
            $("#char-count").css("color", "green");
        } else if (numero < 80 && numero >= 40) {
            $("#char-count").css("color", "yellow");
        } else if (numero < 40 && numero >= 1) {
            $("#char-count").css("color", "red");
        }
    });
});



        /*document.querySelector('#chat-message-input').focus();
        document.querySelector('#chat-message-input').onkeyup = function(e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };*/

        /*document.querySelector('#new-post-button').onclick = function(e) {
            const messageInputDom = document.querySelector('#id_content');
            const message = messageInputDom.value;
            postSocket.send(JSON.stringify({
                'message': message
            }));
            //document.querySelector("#posts").innerHTML = "";
        };*/

//$(document).ready(function() {
//    $("#upload-post").submit(function(e) {
//        const postData = {
//            content: $("#new-post-content").val()
//        };
//
//        $.post("/ajax/new-post/", postData, function (response) {
//            /*let link = "";
//
//            switch (window.location.href) {
//                case "https://www.nekomon.es/":
//                    link = "https://www.nekomon.es/ajax/list-posts-followed.php";
//                    break;
//
//                default:
//                    link = "https://www.nekomon.es/ajax/list-posts.php";
//                    break;
//            }
//
//            fetchPosts(link);
//
//            if (!fetchErrors()) {
//                $("#errors").empty();
//            };*/
//
//            $("#upload-post").trigger("reset");
//        });
//
//        $("#char-count").empty();
//
//        e.preventDefault();
//    });
//
//    $("#new-post-content").keypress(function(e) {
//        let keycode = (e.keyCode ? e.keyCode : e.which);
//
//        if (keycode == "13") {
//            $("#upload-post").submit();
//        };
//    });
//
//    $("#new-post-content").on("keydown keyup", function(e) {
//        $("#char-count").html(140 - this.value.length);
//        let numero = $("#char-count").html();
//
//        if (numero <= 140 && numero >= 80) {
//            $("#char-count").css("color", "green");
//        } else if (numero < 80 && numero >= 40) {
//            $("#char-count").css("color", "yellow");
//        } else if (numero < 40 && numero >= 1) {
//            $("#char-count").css("color", "red");
//        }
//    });
//});