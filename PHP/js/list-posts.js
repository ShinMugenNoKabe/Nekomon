function fetchPosts(link) {
    $.ajax({
        url: link,
        type: "post",
        success: function(response) {
            let posts = JSON.parse(response);
            let template = "";
            posts.forEach(post => {
                template += `
                    <div class="post">
                        <div class='post-header'>
                            <div>
                                <img class='post-pfp' src='images/profile_pictures/${post.profile_picture}'>
                            </div>
                            <div class='post-username-date'>
                                <a href="https://www.nekomon.es/${post.username}">
                                    <p>
                                        ${post.name} 
                                    </p>
                                    <p>
                                        @${post.username}
                                    </p>
                                </a>
                                <p>
                                    ${post.date}
                                </p>
                            </div>
                        </div>
                        <hr>
                        <div class='post-content'>
                            ${post.content}
                        </div>
                        <hr>
                        <i class="fas fa-heart"></i>
                    </div>
                `
            });

            $("#posts").html(template);
        }
    });
};