<?php
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        session_start();

        $jsonString = json_encode($_SESSION["json"]);
        print($jsonString);
        unset($_SESSION["json"]);
    } else {
        header("Location: https://www.nekomon.es/");
    }