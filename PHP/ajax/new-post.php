<?php
    session_start();

    require ("../model/SQLDBConnection.php");
    require ("../model/FlashMessages.php");
    require ("../model/UserDAO.php");
    require ("../model/PostDAO.php");
    require ("../model/Session.php");

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $conn = SQLDBConnection::connect();

        $messages = new FlashMessages();

        $content = $_POST["content"];

        if (strlen(trim($content, " ")) == 0) {
            $messages->addMessage("error_message", "El post no puede estar vacío.");
                        
            $_SESSION["json"] = $messages->showMessages();
        } elseif (strlen($content) > 140) {
            $messages->addMessage("error_message", "La longitud no puede ser mayor de 140 carácteres.");
                        
            $_SESSION["json"] = $messages->showMessages();
        } else {
            $content = filter_var($content, FILTER_SANITIZE_SPECIAL_CHARS);

            $postDAO = new PostDAO($conn);
            $post = new Post();
            $post->setUser_id(Session::obtain_id());
            $post->setContent($content);
            //$newPost = filter_var($newPost, FILTER_SANITIZE_SPECIAL_CHARS);
    
            $postDAO->insert($post);
    
            //$messages->addMessage("content", $content);
        }
    } else {
        //FlashMessages::addMessage("error-not-logged-in", "Debe de iniciar sesión para continuar.");

        header("Location: https://www.nekomon.es/");
    }
