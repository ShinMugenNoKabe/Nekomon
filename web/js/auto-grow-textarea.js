$("#id_content").on('input', function() {
	var scroll_height = $("#id_content").get(0).scrollHeight;

	$("#id_content").css('height', scroll_height + 'px');
});