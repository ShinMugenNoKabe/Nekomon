function fetchPosts(view) {
    $.ajax({
        url: view,
        type: "post",
        success: function(response) {
            let posts = response;
            let template = "";
            posts.forEach(post => {
                template += `
                    <div class="post">
                        <div class='post-header'>
                            <div>
                                <img class='post-pfp' src="/web/images/profile_pictures/${post.user.profile_picture}">
                            </div>
                            <div class='post-username-date'>
                                <a href="/${post.user.username}">
                                    <p>
                                        ${post.user.name}
                                    </p>
                                    <p>
                                        @${post.user.username}
                                    </p>
                                </a>
                                <p>
                                    <a href="/posts/${post.id}">
                                        ${new Date(post.created_at).toLocaleDateString()}
                                        ${new Date(post.created_at).toLocaleTimeString()}
                                    </a>
                                </p>
                            </div>
                        </div>
                        <hr>
                        <div class='post-content'>
                            ${post.content}
                        </div>
                        <hr>`
                        + getImage(post) + `
                        <form id='like-post'>
                            <input type='hidden' value='${post.id}'>
                            <i class="fas fa-heart like-icon"></i>
                        </form>
                    </div>
                `
            });

            $("#posts").html(template);
        }
    });
};

function getImage(post) {
    if (post.image === "") {
        return "";
    }

    return `
        <div class="post-image">
            <img src='https://i.imgur.com/` + post.image + `.png' alt="Image attached to the post">
        </div>
        <hr>
    `
}