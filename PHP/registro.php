<?php
    session_start();
    
    require ("model/Session.php");
    require ("model/FlashMessages.php");

    if (Session::exists()) {
        header("Location: https://www.nekomon.es");
    }
?>

<!DOCTYPE html>
<html lang="es-ES">
<head>
    <meta charset="UTF-8">
    <title>Registro - Nekomon</title>
    <link rel="icon" type="image/png" href="https://www.nekomon.es/images/neko.png">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="https://www.nekomon.es/css/login-register-forms.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
</head>
<body>
    <main>
        <div id="form-container">
            <form id="register-form">
                <img src="https://www.nekomon.es/images/neko.png" id="nekomon-logo">
                <p id="top-text">Registro</p>

                <!-- Campo de email  -->
                <div class="input-row">
                    <input type="text" class="input-text" id="email" value="<?php if(isset($user_name_email)) print $user_name_email ?>" placeholder="E-mail">
                </div>

                <!-- Campo de nombre de usuario  -->
                <div class="input-row">
                    <input type="text" class="input-text" id="username" value="<?php if(isset($user_name_email)) print $user_name_email ?>" placeholder="Nombre de usuario">
                </div>

                <!-- Campo de contraseña -->
                <div class="input-row">
                    <input type="password" class="input-text" id="password" value="<?php if(isset($password)) print $password ?>" placeholder="Contraseña">
                </div>

                <!-- Campo de repite contraseña -->
                <div class="input-row">
                    <input type="password" class="input-text" id="password2" value="<?php if(isset($password)) print $password ?>" placeholder="Repita la contraseña">
                </div>
                
                <!-- Errores -->
                <div id="errors"></div>
            </form> 

            <div class="buttons-links">
                <button class="big-button" type="submit" form="register-form">Registrarse</button>
                <div class="link">
                    <a href="https://www.nekomon.es/">Regresar</a>
                </div>
            </div>
        </div>
    </main>
    <script type="text/javascript" src="https://www.nekomon.es/js/register.js"></script>
    <script type="text/javascript" src="https://www.nekomon.es/js/fetch-errors.js"></script>
</body>
</html>
