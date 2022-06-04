//$(document).ready(function() {
    if ($("#follow-unfollow-button").html() === "Seguir") {
    
        $("#follow-unfollow").submit(function(e) {
                const postData = {
                    idFollower: <?= Session::obtain_id() ?>,
                    idFollowed: <?= $user->getId() ?>,
                };
                $.post("https://www.nekomon.es/ajax/follow.php", postData, function (response) {
                    $("#follow-unfollow").trigger("reset");
                });

                $("#follow-unfollow-button").html("Dejar de seguir");
                
            e.preventDefault();
        });
    } else {
        $("#follow-unfollow").submit(function(e) {
                const postData = {
                    idFollower: <?= Session::obtain_id() ?>,
                    idFollowed: <?= $user->getId() ?>,
                };
                $.post("https://www.nekomon.es/ajax/unfollow.php", postData, function (response) {
                    $("#follow-unfollow").trigger("reset");
                });

                $("#follow-unfollow-button").html("Seguir");
                
            e.preventDefault();
        });
    }
//});