<?php
    session_start();

    require ("../model/SQLDBConnection.php");
    require ("../model/FlashMessages.php");
    require ("../model/UserDAO.php");
    require ("../model/FollowerDAO.php");
    require ("../model/Session.php");

    if (Session::obtain_id() && isset($_POST["idFollower"])) {
        $conn = SQLDBConnection::connect();

        $id_user_followed = $_POST['id_user_followed'];

        $folDAO = new FollowerDAO($conn);
        $folDAO->insert($id_user_followed, Session::obtain_id());
    } else {
        FlashMessages::addMessage("error-not-logged-in", "Debe de iniciar sesión para continuar.");
    }