<?php

/**
 * Clase para manejo de sesiones de usuario en nuestra página (inicio de sesión, cierre de sesión, si existe la sesión, etc.)
 *
 * @author Rufino
 */
class Session {
    static public function start($id){
        $_SESSION['id_session_user'] = $id;
    }
    
    static public function exists() {
        return isset($_SESSION['id_session_user']);
    }
    
    static public function close($id){
        unset($_SESSION['id_session_user']);
        setcookie("user", $id, time() - 3600);
    }
    
    static public function obtain_id(){
        if (isset($_SESSION['id_session_user'])) {
            return $_SESSION['id_session_user'];
        } else {
            return false;
        }
    }

    static public function setRequestedUserName($requested_username) {
        $_SESSION['requested_username'] = $requested_username;
    }

    static public function getRequestedUserName() {
        return $_SESSION['requested_username'];
    }
}
