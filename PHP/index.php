<?php
    session_start();
    
    require ("model/SQLDBConnection.php");
    require ("model/FlashMessages.php");
    require ("model/UserDAO.php");
    require ("model/PostDAO.php");
    require ("model/Session.php");

    //$conn = SQLDBConnection::connect();

    if (isset($_COOKIE['uid']) && !Session::exists()) {
        $cookie_id = filter_var($_COOKIE['uid'], FILTER_SANITIZE_SPECIAL_CHARS);

        $conn = SQLDBConnection::connect();

        $userDAO = new UserDAO($conn);

        $user = $userDAO->findByCookieId($cookie_id);
        
        if ($user != false) {
            Session::start($user->getId());

            print(Session::obtain_id());

            $posts = $user->getFollowerd_users_posts($conn);
        }
    }

    // Generamos token para seguridad del borrado
    $_SESSION['token'] = md5(time() + rand(0, 999));
    $token = $_SESSION['token'];
?>

<!DOCTYPE html>
<html lang="es-ES">
<head>
    <meta charset="utf-8">
    <link rel="icon" type="image/png" href="https://www.nekomon.es/images/neko.png">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
    <?php
        if (!Session::exists()) {
            print("<link rel='stylesheet' type='text/css' href='https://www.nekomon.es/css/login-register-forms.css'>");
            print("<title>Iniciar sesión - Nekomon</title>");
        } else {
            print("<link rel='stylesheet' type='text/css' href='https://www.nekomon.es/css/main.css'>");
            print("<link rel='stylesheet' type='text/css' href='https://www.nekomon.es/css/fontawesome.min.css'>");
            print("<title>Página principal - Nekomon</title>");
        }
    ?>
</head>
<body>
    <?php if (!Session::exists()): ?>
    <!-- Formulario de inicio de sesión si no se ha iniciado sesión -->
        <main>
            <div id="form-container">
                <form id="log-in-form">
                    <img src="https://www.nekomon.es/images/neko.png" id="nekomon-logo">
                    <p id="top-text">Iniciar sesión</p>

                    <!-- Campo de usuario  -->
                    <div class="input-row">
                        <input type="text" class="input-text" id="username" value="<?php if(isset($_SESSION["username"])) { print $_SESSION["username"]; unset($_SESSION["username"]); } ?>" placeholder="Nombre de usuario">
                    </div>

                    <!-- Campo de contraseña -->
                    <div class="input-row">
                        <input type="password" class="input-text" id="password" placeholder="Contraseña">
                    </div>

                    <!-- Errores -->
                    <div id="errors"></div>
                </form>

                <div class="buttons-links">
                    <button class="big-button" type="submit" form="log-in-form">Entrar</button>
                    <div class="link">
                        ¿No posee una cuenta? <a href="https://www.nekomon.es/registro.php">Registrarse</a>
                    </div>
                </div>
            </div>
        </main>
        <script type="text/javascript" src="https://www.nekomon.es/js/log-in.js"></script>
        <script type="text/javascript" src="https://www.nekomon.es/js/fetch-errors.js"></script>
    <?php else: ?>
    <!-- Contenido de la página si se ha iniciado sesión -->
        <?php
            include("contenido/user-nav.php");
            include("contenido/new-post-html.php");
        ?>
        <div id="posts" class="animated animatedFadeInUp fadeInUp"></div>
        <script type="text/javascript" src="https://www.nekomon.es/js/fontawesome.min.js"></script>
        <script type="text/javascript" src="https://www.nekomon.es/js/list-posts.js"></script>
        <script type="text/javascript" src="https://www.nekomon.es/js/upload-post.js"></script>
        <script type="text/javascript" src="https://www.nekomon.es/js/fetch-errors.js"></script>
        <script type="text/javascript">
            fetchPosts("https://www.nekomon.es/ajax/list-posts-followed.php");
        </script>
    <?php endif; ?>
</body>
</html>