function jsonErrors(data) {
    errors = data.responseJSON.error[0];

    let error_list = "<ul class='errorlist'>";

    for (error in errors) {
        let error_message = errors[error];
        error_list = (error_list + "<li>" + error_message + "</li>");
    }

    error_list = (error_list + "</ul>");

    $("#errors").html(error_list);
}