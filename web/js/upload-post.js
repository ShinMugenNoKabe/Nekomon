let post_box = $('#upload-post');

post_box.submit(function () {
    $.ajax({
        type: "post",
        url: "/ajax/new-post/",
        data: post_box.serialize(),
        success: function(data) {
            fetchPosts("ajax/list-posts-main/");
            $('#id_content').val("");
            $("#char-count").html("");
        },
        error: function(data) {
            $("#errors").html("<div class='flash-message'>" + data.responseJSON.error + "</div>");
        }
    });
    return false;
});

$(document).ready(function() {
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