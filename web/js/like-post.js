$(".like-post-icon").click(function() {
    const id_post = $(this).attr("id");

    $.ajax({
        type: "post",
        url: "/ajax/like-post/",
        data: {
            id_post
        }
        success: function(data) {
            /*if (data == "true") {

            } else {

            }*/
        },
        /*error: function(data) {
            $("#errors").html("<div class='flash-message'>" + data.responseJSON.error + "</div>");
        }*/
    });
});