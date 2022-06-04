<?php
    require ("model/PostDAO.php");
    require ("model/FollowDAO.php");

    $usuDAO = new UserDAO($conn);

    $userSession = 0;

    if (Session::exists()) {
        $userSession = $usuDAO->find(Session::obtain_id());
    }
    
    $user = $usuDAO->findByUsername(Session::getRequestedUserName());
    $posts = $user->getPosts($conn);
    $followed_users = $user->getFollowed_users($conn);

    $isFollowing = false;

    if (Session::exists() && $userSession->isFollowing($conn, $user->getId())) {
        $isFollowing = true;
    }
?>

<main>
    <div class="profile-header">
        <img class='profile-pfp' src="images/profile_pictures/<?= $user->getProfile_picture() ?>">

        <div class="profile-username">
            <p>
                <?= $user->getName() ?>
            </p>
        </div>

        <div class="profile-at">
            <p>
                @<?= $user->getUsername() ?>
            </p>
        </div>

        <div class="profile-description">
            <p>
                <?= $user->getDescription() ?>
            </p>
        </div>

        <div class="profile-register-date">
            <p>
                Fecha de registro: <?= $user->getRegistration_date() ?>
            </p>
        </div>

        <div>
            <?php if ($user->getId() == Session::obtain_id()): ?>
                <form id="edit-profile" method="post" action="edit-profile.php" class="profile-button-container">
                    <button form="edit-profile" class="profile-button">Editar perfil</button>
                </form>
            <?php else: ?>
                <form id="follow-unfollow" class="profile-button-container">
                    <button form="follow-unfollow" class="profile-button" id="follow-unfollow-button">
                        <?php
                            if (!$isFollowing) {
                                print("Seguir");
                            } else {
                                print("Dejar de seguir");
                            }
                        ?>
                    </button>
                </form>
            <?php endif; ?>
        </div>
    </div>

    <?php
        if (Session::obtain_id() == $user->getId()) {
            include("contenido/new-post-html.php");
        }
    ?>
    <div id="posts" class="animated animatedFadeInUp fadeInUp"></div>
</main>
<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
<script src="https://www.nekomon.es/js/fontawesome.min.js"></script>
<script type="text/javascript" src="https://www.nekomon.es/js/list-posts.js"></script>
<script type="text/javascript" src="https://www.nekomon.es/js/upload-post.js"></script>
<script type="text/javascript" src="https://www.nekomon.es/js/fetch-errors.js"></script>
<script type="text/javascript">
    fetchPosts("https://www.nekomon.es/ajax/list-posts.php");
</script>
<script type="text/javascript">
    $(document).ready(function() {
        $("#follow-unfollow").submit(function(e) {
            const postData = {
                id_user_followed: <?= $user->getId() ?>,
                action: $("#follow-unfollow-button").html()
            };

            $.post("https://www.nekomon.es/ajax/follow-unfollow.php", postData, function (response) {
                $("#follow-unfollow").trigger("reset");
            });

            let link = function() {
                if ($("#follow-unfollow-button").html() === "Seguir") {
                    $("#follow-unfollow-button").html("Dejar de seguir");
                } else {
                    $("#follow-unfollow-button").html("Seguir");
                }
            };
            
            link();
            
            e.preventDefault();
        });
    });
</script>