function jsonErrors(data) {
    errors = JSON.parse(data.responseJSON.errors);
    let error_list = "<ul class='errorlist'>";

    for (error in errors['__all__']) {
        let error_message = errors['__all__'][error]['message'];
        error_list = (error_list + "<li>" + error_message + "</li>");
    }

    error_list = (error_list + "</ul>");

    $("#errors").html(error_list);
}

