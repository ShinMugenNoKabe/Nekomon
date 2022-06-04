<?php
    $conn = SQLDBConnection::connect();
?>

<nav>
    <a href="https://www.nekomon.es"><img id="nav-logo" src="https://www.nekomon.es/images/neko.png" title="Inicio"></a>

    <?php
        if (Session::exists()):
            $userDAO = new UserDAO($conn);
            $user = $userDAO->find(Session::obtain_id());
    ?>
    
    <div id="nav-username-logout">
        <a href="<?= $user->getUsername(); ?>" class="nav-username-and-pfp">
            <div class="nav-user-data">
                <span class="nav-username"><?= $user->getUsername(); ?></span>
                <?php $profile_picture = $user->getProfile_picture(); ?>
                <img class='profile-picture-nav' src="https://www.nekomon.es/images/profile_pictures/<?= $profile_picture ?>">
            </div>
        </a>

        <form action="https://www.nekomon.es/logout.php" id="logout">
            <button id="nav-logout-button" form="logout">Cerrar sesión</button>
        </form>
    </div>        

    <?php else: ?>
        <div class="nav-user-data">
            <a href="https://www.nekomon.es">Iniciar sesión</a>
        </div>
    <?php endif; ?>
    
</nav>