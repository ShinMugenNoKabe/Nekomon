$(document).ready(function() {
    $("#upload-post").submit(function(e) {
        const postData = {
            content: $("#new-post-content").val()
        };

        $.post("https://www.nekomon.es/ajax/new-post.php", postData, function (response) {
            let link = "";

            switch (window.location.href) {
                case "https://www.nekomon.es/":
                    link = "https://www.nekomon.es/ajax/list-posts-followed.php";
                    break;
                
                default:
                    link = "https://www.nekomon.es/ajax/list-posts.php";
                    break;
            }

            fetchPosts(link);

            if (!fetchErrors()) {
                $("#errors").empty();
            };

            $("#upload-post").trigger("reset");
        });

        $("#char-count").empty();
        
        e.preventDefault();
    });

    $("#new-post-content").keypress(function(e) {
        let keycode = (e.keyCode ? e.keyCode : e.which);

        if (keycode == "13") {
            $("#upload-post").submit();
        };
    });

    $("#new-post-content").on("keydown keyup", function(e) {
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