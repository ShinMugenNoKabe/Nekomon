<div class="post animated animatedFadeInUp fadeInUp">
    <div class='post-header'>
        <div>
            <img class='post-pfp' src='images/profile_pictures/<?= $user->getProfile_picture(); ?>'>
        </div>
        <div class='post-username-date'>
                <p>
                <a href="<?= $user->getUsername(); ?>">
                    <?= $user->getUsername(); ?>
                </a>
            </p>
         </div>
    </div>
    <hr>
    <form id="upload-post">
        <div>
            <textarea id="new-post-content" name="new-post" placeholder="Nuevo post" maxlength="140"></textarea>
        </div>
        <button id="new-post-button" form="upload-post">Subir nuevo post</button>
        <div id="char-count"></div><br>
        <div id="errors"></div>
    </form>
</div>