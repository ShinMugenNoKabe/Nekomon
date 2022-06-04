<?php
    session_start();
    
    require ("model/SQLDBConnection.php");
    require ("model/UserDAO.php");
    require ("model/Session.php");

    if (empty($_GET['username'])) {
        header("Location: https://www.nekomon.es");
    } else {
        $userDAO = new UserDAO(SQLDBConnection::connect());
        $requested_username = $_GET['username'];
        $requested_username = substr($requested_username, 1, strlen($requested_username));
        $user = $userDAO->findByUsername($requested_username);

        if ($user != null) {
            Session::setRequestedUserName($user->getUsername());
        } else {
            header("Location: https://www.nekomon.es");
        }
    }
?>

<!DOCTYPE html>
<html lang="es-ES">
    <head>
        <meta charset="utf-8">
        <title><?= $user->getName(); ?> - Nekomon</title>
        <link rel="icon" type="image/png" href="https://www.nekomon.es/images/neko.png">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="https://www.nekomon.es/css/main.css">
        <link rel="stylesheet" type="text/css" href="https://www.nekomon.es/css/fontawesome.min.css">
    </head>
    <body>
        <?php
            include("contenido/user-nav.php");
            include("contenido/user-profile.php");
        ?>
    </body>
</html>

