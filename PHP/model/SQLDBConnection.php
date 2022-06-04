<?php

class SQLDBConnection {

    public static function connect(): mysqli {
        // Crear la conexión
        $conn= new mysqli('localhost', "root", '', "nekomon", "3306");
            
        // Comprobar la conexión
        if ($conn->connect_error) {
            // Termina el programa e imprime el mensaje
            die("Error al conectar con MySQL " . $conn->connect_error);
        }
        
        return $conn;
    }
}