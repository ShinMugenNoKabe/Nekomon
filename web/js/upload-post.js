let post_box = $('#upload-post');

post_box.submit(function (e) {
    let formData = new FormData();
    let content = $(post_box).children("textarea[name='content']").val();
    let image = $(post_box).children("input[name='image']")[0];
    let csrftoken = $(post_box).children("input[name='csrfmiddlewaretoken']").val();

    formData.append("content", content);
    formData.append("image", image.files[0]);
    formData.append("csrfmiddlewaretoken", csrftoken);

    $.ajax({
        type: "post",
        enctype: 'multipart/form-data',
        url: "/ajax/new-post/",
        data: formData,
        processData: false,
        contentType: false,
        success: function(data) {
            fetchPosts("ajax/list-posts-main/");
            $('#id_content').val("");
            $("#char-count").html("");
        },
        error: function(data) {
            //data = JSON.des
            console.log(data)
            $("#errors").html("<div class='flash-message'>" + data.responseJSON.error + "</div>");
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