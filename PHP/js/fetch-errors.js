function fetchErrors() {
    $.ajax({
        url: "https://www.nekomon.es/ajax/errors.php",
        type: "post",
        success: function(response) {
            let errors = JSON.parse(response);

            if (errors == null) {
                return false;
            }

            let template = "";
            errors.forEach(error => {
                template += `
                        <div class='flash-message'>${error.error_message}</div>
                    `
            });

            if (template == "") {
                /*xhttp.open("GET", "https://www.nekomon.es/setcookie.php", true);
                xhttp.send();*/
                location.reload();
            } else {
                $("#errors").html(template);
            }
        }
    });
}