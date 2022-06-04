<?php

    require ("model/UserDAO.php");
    require ("model/SQLDBConnection.php");

    $usuDAO = new UserDAO(SQLDBConnection::connect());
    $users = $usuDAO->findAll();

    $cabeceras = "From: Nekomon.es <nekomon.es@gmail.com>" . "\r\n";
    $cabeceras .= "MIME-Version: 1.0" . "\r\n";
    $cabeceras .= "Content-type: text/html; charset=utf-8" . "\r\n";

    foreach($users as $user) {
        mail($user->getEmail(), "HOLA", "<h1>QUE PASAAAAAAAAAAAAAAAAAAAAA</h1>", $cabeceras);
    }
    
?>