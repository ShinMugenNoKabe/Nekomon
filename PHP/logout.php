<?php
    session_start();
    require ("model/Session.php");
    
    Session::close(Session::obtain_id());

    // Borrar la cookie creándola de nuevo pero caducada
    setcookie('uid', (time() - 5));
    
    header("Location: https://www.nekomon.es");