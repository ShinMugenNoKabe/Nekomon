<?php
    session_start();

    require ("../model/SQLDBConnection.php");
    require ("../model/FlashMessages.php");
    require ("../model/UserDAO.php");
    require ("../model/Session.php");

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $email = $_POST['email'];
        $username = $_POST['username'];
        $password = $_POST['password'];
        $password2 = $_POST['password2'];

        $error = false;

        $messages = new FlashMessages();

        if (empty($email)) {
            $messages->addMessage("error_message", "Debe de introducir una dirección de correo electrónico.");
            $error = true;
        } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $messages->addMessage("error_message", "El formato de la dirección de correo electrónico no es correcto.");
            $error = true;
        }

        if (empty($username)) {
            $messages->addMessage("error_message", "Debe de introducir un nombre de usuario.");
            $error = true;
        } elseif (!(str_replace(' ', '', $username) == $username) || !(preg_replace('/[^A-Za-z0-9\-]/', '', $username) == $username)) {
            $messages->addMessage("error_message", "El nombre de usuario no puede contener espacios en blanco ni carácteres especiales.");
            $error = true;
        }

        if (empty($password)) {
            $messages->addMessage("error_message", "Debe de introducir una contraseña.");
            $error = true;
        } else if ($password != $password2) {
            $messages->addMessage("error_message", "Las contraseñas introducidas no coinciden.");
            $error = true;
        }

        if ((empty($password) == false) && (strlen($password) < 6)) {
            $messages->addMessage("error_message", "La contraseña debe de tener un mínimo de 6 caracteres de longitud.");
            $error = true;
        }

        // preg_match() comprueba si tiene un carácter especial
        /*if ((empty($password) == false) && (preg_match("/[\'^£$%&*()}{@#~!¡?¿><,|=_+¬-]/", $password) == false)) {
            FlashMessages::addMessage("error-password-char", "La contraseña debe de tener como mínimo un carácter especial.");
            $error = true;
        }*/

        if ($error == false) {
            // Realiza la consulta
            $conn = SQLDBConnection::connect();
            
            $userDAO = new UserDAO($conn);
            $user = $userDAO->findByEmailOrUsername($email, $username);

            if ($user == null) {
                
                function getRealIP() {
                    if (isset($_SERVER["HTTP_CLIENT_IP"])) {
                        return $_SERVER["HTTP_CLIENT_IP"];
                    } elseif (isset($_SERVER["HTTP_X_FORWARDED_FOR"])) {
                        return $_SERVER["HTTP_X_FORWARDED_FOR"];
                    } elseif (isset($_SERVER["HTTP_X_FORWARDED"])) {
                        return $_SERVER["HTTP_X_FORWARDED"];
                    } elseif (isset($_SERVER["HTTP_FORWARDED_FOR"])) {
                        return $_SERVER["HTTP_FORWARDED_FOR"];
                    } elseif (isset($_SERVER["HTTP_FORWARDED"])) {
                        return $_SERVER["HTTP_FORWARDED"];
                    } else {
                        return $_SERVER["REMOTE_ADDR"];
                    }
                }

                $user = new User();

                //$username = filter_var($username, FILTER_SANITIZE_SPECIAL_CHARS);
                $username = htmlentities($username);
                $user->setUsername($username);

                $email = filter_var($email, FILTER_SANITIZE_EMAIL);
                $user->setEmail($email);
                
                $encryptedPassword = password_hash($password, PASSWORD_BCRYPT);
                $user->setPassword($encryptedPassword);

                // Generamos un código aleatorio sha1 y lo guardamos en la BD
                // Nombre, valor, expira (1 semana)
                $user->setCookie_id(sha1(time() + rand()));

                $user->setRegistration_ip(getRealIP());

                $userDAO->insert($user);
                Session::start($user->getId());

                // Creamos la cookie en el navegador del cliente con el mismo código
                setcookie("uid", $user->getCookie_id(), (time() + (60 * 60 * 24 * 30)));

                header("Location: https://www.nekomon.es");  
            } else {
                $messages->addMessage("error_message", "El usuario o dirección de correo electrónico introducido ya se encuentran registrados."); 

                header("Location: https://www.nekomon.es/registro.php"); 
            }
        } else {
            header("Location: https://www.nekomon.es/registro.php"); 
        }
        
        $_SESSION["json"] = $messages->showMessages();
    } else {
        header("Location: https://www.nekomon.es");
    }
    
    // Calculamos un token
    $token = md5(time() + rand (0, 999));
    $_SESSION['token'] = $token;
