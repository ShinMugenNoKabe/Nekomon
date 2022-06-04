<?php

include("User.php");

class UserDAO {

    private $conn;
    
    public function __construct($conn) {
        $this->conn = $conn;
    }
        
    /**
     * Devuelve el usuario de la BD según su ID
     * @param type $id ID del usuario
     * @return \User Usuario de la BD o null si no existe
     */
    public function find($id): User {
        $sql = "SELECT * from users where id = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("i", $id);

        $stmt->execute();
        $result = $stmt->get_result();

        // fetch_object() devuelve un objeto de una clase
        return $result->fetch_object("User");
    }

    /**
     * Devuelve todos los usuarios de la BD
     * @param type $column Campo de la BD por el que se van a ordenar
     * @param type $order Tipo de orden (ASC o DESC)
     * @return array Array de objetos de la clase Usuario
     */
    public function findAll($column = "id", $order = "ASC"): Array {
        $sql = "SELECT * from users order by $column $order";

        if (!$result = $this->conn->query($sql)) {
            die("Error en la SQL: " . $this->conn->error);
        }
        
        $arrray_users = array();
        while ($user = $result->fetch_object("User")) {
            $arrray_users[] = $user;
        }
        
        return $arrray_users;
    }

    /**
     * Inserta el usuario en la BD
     * @param type $user Usuario a insertar
     * @return true si se ha insertado bien o false o si no se ha insertado
     */
    public function insert($user) {
        if (!$user instanceof User) {
            return false;
        }

        $username = $user->getUsername();
        $email = $user->getEmail();
        $password = $user->getPassword();
        $cookie_id = $user->getCookie_id();
        $ip = $user->getRegistration_ip();
        
        $sql = "INSERT into users (username, email, password, name, cookie_id, registration_ip) values (?, ?, ?, ?, ?, ?)";

        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param("ssssss", $username, $email, $password, $username, $cookie_id, $ip);

        $stmt->execute();

        // Guarda el id que se le ha asignado la base de datos al objeto en la variable $id
        $user->setId($this->conn->insert_id);

        return true;
    }
    
    /**
     * Actualiza el usuario de la BD
     * @param type $user Usuario a actualizar
     * @return true si se ha actualizado bien o false o si no se ha actualizado
     */
    public function update($user) {
        if (!$user instanceof User) {
            return false;
        }

        $id = $user->getId();
        $email = $user->getEmail();
        $username = $user->getUsername();
        $password = $user->getPassword();
        $profile_picture = $user->getProfile_picture();
        $name = $user->getName();
        $description = $user->getDescription();
        $cookie_id = $user->getCookie_id();

        $sql = "UPDATE users set "
            . "email = ?, username = ?, password = ?, profile_picture = ?, name = ?, description = ?, cookie_id = ? "
            . "where id = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("sssssssi", $email, $username, $password, $profile_picture, $name, $description, $cookie_id, $id);
        $stmt->execute();
        $result = $stmt->get_result();

        // affected_rows comprueba si se ha borrado 1 línea
        if ($this->conn->affected_rows == 1) {
            return true;
        } else {
            return false;
        }
    }
    
    /**
     * Borra el usuario de la BD
     * @param type $user Usuario a borrar
     * @return true si se ha borrado bien o false o si no se ha borrado
     */
    public function delete($user) {
        // Comprobamos que el parámetro no es nulo y si es de la clase Usuario
        if ($user == null || get_class($user) != "User") {
            return false;
        }

        $id = $user->getId();
        
        $sql = "DELETE from users where id = ? ";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("i", $id);
        $stmt->execute();
        $result = $stmt->get_result();

        // affected_rows comprueba si se ha borrado 1 línea
        if ($this->conn->affected_rows == 1) {
            return true;
        } else {
            return false;
        }
    }
        
    /**
     * Devuelve el usuario de la BD según su email
     * @param type $email Email del usuario
     * @return \User Usuario de la BD o null si no existe
     */
    public function findByEmail($email) {
        if (!is_string($email)) {
            return false;
        }

        $sql = "SELECT * from users where email = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("s", $email);

        $stmt->execute();
        $result = $stmt->get_result();

        // fetch_object() devuelve un objeto de una clase
        return $result->fetch_object("User");
    }

    /**
     * Devuelve el usuario de la BD según su username
     * @param type $username username del usuario
     * @return \User Usuario de la BD o null si no existe
     */
    public function findByUsername($username) {
        if (!is_string($username)) {
            return false;
        }

        $sql = "SELECT * from users where username = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("s", $username);

        $stmt->execute();
        $result = $stmt->get_result();

        // fetch_object() devuelve un objeto de una clase
        return $result->fetch_object("User");
    }

    /**
     * Devuelve el usuario de la BD según su email o username
     * @param type $username username del usuario
     * @return \User Usuario de la BD o null si no existe
     */
    public function findByEmailOrUsername($email, $username) {
        if (!is_string($email) || !is_string($username)) {
            return false;
        }

        $sql = "SELECT * from users where email = ? or username = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("ss", $email, $username);

        $stmt->execute();
        $result = $stmt->get_result();

        // fetch_object() devuelve un objeto de una clase
        return $result->fetch_object("User");
    }

    /**
     * Devuelve el usuario de la BD según su username
     * @param type $username username del usuario
     * @return \User Usuario de la BD o null si no existe
     */
    public function findByCookieId($cookie_id) {
        if (!is_string($cookie_id)) {
            return false;
        }

        $sql = "SELECT * from users where cookie_id = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("s", $cookie_id);

        $stmt->execute();
        $result = $stmt->get_result();

        // fetch_object() devuelve un objeto de una clase
        return $result->fetch_object("User");
    }

    public function getNewID() {
        $sql= "SELECT (max(id)+1) as newId from users";

        if (!$result = $this->conn->query($sql)) {
            die("Error al ejecutar la consulta: " . $this->conn->error);
        }

        return $result->fetch_assoc();
    }
}
