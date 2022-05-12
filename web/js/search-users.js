const searchUsersInput = $('#search-users-input');

searchUsersInput.on("input", function () {
    $.ajax({
        type: "post",
        url: "/ajax/search-users/",
        data: {
            "input": searchUsersInput.val()
        },
        success: function(data) {
            console.log(data);
        },
        error: function(data) {
            //
        }
    });
    return false;
});