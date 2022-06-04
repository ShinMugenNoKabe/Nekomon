<?php
    session_start();

    require ("../model/SQLDBConnection.php");
    require ("../model/FlashMessages.php");
    require ("../model/UserDAO.php");
    require ("../model/FollowDAO.php");
    require ("../model/Session.php");

    if (Session::obtain_id() && isset($_POST["id_user_followed"])) {
        $conn = SQLDBConnection::connect();

        $id_user_followed = $_POST["id_user_followed"];
        $action = $_POST["action"];

        $folDAO = new FollowDAO($conn);
        $follow = new Follow();
        $follow->setUser_id_follower(Session::obtain_id());
        $follow->setUser_id_followed($id_user_followed);

        if ($action == "Seguir") {
            $folDAO->insert($follow);
        } else {
            $folDAO->deleteByFollower($follow);
        }
    } else {
        $messages = new FlashMessages();
        $messages->addMessage("error_message", "Debe de iniciar sesión para continuar.");
        header("Location: https://www.nekomon.es/");
        /*echo json_encode(['location'=>'https://www.nekomon.es/']);
        exit;*/
    }