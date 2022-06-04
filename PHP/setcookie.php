<?php
    session_start();

    require("model/SQLDBConnection.php");
    require("model/Session.php");
    require("model/UserDAO.php");

    $userDAO = new UserDAO(SQLDBConnection::connect());

    $user = $userDAO->find(Session::obtain_id());
    
    $user->setCookie_id(sha1(time() + rand()));
    $userDAO->update($user); 

    setcookie("uid", $user->getCookie_id(), (time() + (60 * 60 * 24 * 30)));

    //print($_COOKIE["uid"]);
?>