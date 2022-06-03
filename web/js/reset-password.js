let passwordForm = $('#reset-form');

passwordForm.submit(function () {
    $("#errors").html("");

    let resetButton = $("#reset-button");
    let spinLoadIcon = $("#spin-load-icon");

    // Disable the reset button
    resetButton.attr("disabled", true);

    // Show the loading icon
    spinLoadIcon.attr("hidden", false);
});