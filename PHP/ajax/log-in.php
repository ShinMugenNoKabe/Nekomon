<?php
    session_start();

    require ("../model/SQLDBConnection.php");
    require ("../model/FlashMessages.php");
    require ("../model/UserDAO.php");
    require ("../model/Session.php");

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $username = $_POST['username'];
        $password = $_POST['password'];

        $error = false;

        $messages = new FlashMessages();

        if (empty($username)) {
            $messages->addMessage("error_message", "Debe de introducir un nombre de usuario.");
            $error = true;  
        } elseif (!(str_replace(' ', '', $username) == $username) || !(preg_replace('/[^A-Za-z0-9\-]/', '', $username) == $username)) {
            $messages->addMessage("error_message", "El formato del nombre de usuario no es correcto.");
            $error = true; 
        }

        if (empty($password)) {
            $messages->addMessage("error_message", "Debe de introducir una contraseña.");
            $error = true;  
        }

        if ($error == false) {
            $conn = SQLDBConnection::connect();

            $username = filter_var($username, FILTER_SANITIZE_SPECIAL_CHARS);

            // Realiza la consulta
            $userDAO = new UserDAO($conn);
            $user = $userDAO->findByUsername($username);

            if ($user != null && $user->getPassword() == password_verify($password, $user->getPassword())) {
                Session::start($user->getId());

                $user->setCookie_id(sha1(time() + rand()));
                $userDAO->update($user);

                setcookie("uid", $user->getCookie_id(), time() + (60 * 60 * 24 * 30));

                //header("Location: https://www.nekomon.es/");
            } else {
                $messages->addMessage("error_message", "No se ha encontrado el usuario o no coincide con la contraseña.");
            }
        }

        $_SESSION["json"] = $messages->showMessages();
    } else {
        header("Location: https://www.nekomon.es/");
    }