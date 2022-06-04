<?php

include("Follow.php");

class FollowDAO {

    private $conn;
    
    public function __construct($conn) {
        $this->conn = $conn;
    }
        
    /**
     * Devuelve el follow de la BD
     * @param type $id ID del follow
     * @return \User Follow de la BD o null si no existe
     */
    public function find($id): Follow {
        if (!is_int($id)) {
            return false;
        }

        $sql = "SELECT * from follows where id = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("i", $id);

        $stmt->execute();
        $result = $stmt->get_result();

        // fetch_object() devuelve un objeto de una clase
        return $result->fetch_object("Follow");
    }

    /**
     * Devuelve todos los follow de la BD
     * @param type $column Campo de la BD por el que se van a ordenar
     * @param type $order Tipo de orden (ASC o DESC)
     * @return array Array de objetos de la clase Follow
     */
    public function findAll($column = "id", $order = "ASC"): Array {
        if (!is_string($column) || !is_string($order)) {
            return false;
        }

        $sql = "SELECT * from follows order by ? ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("ss", $column, $order);

        $stmt->execute();
        $result = $stmt->get_result();

        // fetch_object() devuelve un objeto de una clase
        return $result->find_all(0, $this->conn->fetch_object("Follow"));
    }

    /**
     * Inserta el follow en la BD
     * @param type $follow Follow a insertar
     * @return true si se ha insertado bien o false o si no se ha insertado
     */
    public function insert($follow) {
        if (!$follow instanceof Follow) {
            return false;
        }

        $id_user_follower = $follow->getUser_id_follower();
        $id_user_followed = $follow->getUser_id_followed();

        $sql = "INSERT into follows (user_id_follower, user_id_followed) values (?, ?)";

        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param("ii", $id_user_follower, $id_user_followed);

        $stmt->execute();

        // Guarda el id que se le ha asignado la base de datos al objeto en la variable $id
        $follow->setId($this->conn->insert_id);

        return true;
    }
    
    /**
     * Actualiza el follow de la BD
     * @param type $follow Follow a actualizar
     * @return true si se ha actualizado bien o false o si no se ha actualizado
     */
    public function update($follow) {
        if (!$follow instanceof Follow) {
            return false;
        }

        $id_user_follower = $follow->getUser_id_follower();
        $id_user_followed = $follow->getUser_id_followed();
        $id = $follow->getId();

        $sql = "UPDATE follows set "
            . "user_id_follower = ?, user_id_followed = ? "
            . "where id = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("iii", $id_user_follower, $id_user_followed, $id);
        $stmt->execute();
        $result = $stmt->get_result();

        // affected_rows comprueba si se ha actualizado 1 línea
        if ($this->conn->affected_rows > 0) {
            return true;
        } else {
            return false;
        }
    }
    
    /**
     * Borra el follow de la BD
     * @param type $follow Follow a borrar
     * @return true si se ha borrado bien o false o si no se ha borrado
     */
    public function delete($follow) {
        // Comprobamos que el parámetro no es nulo y si es de la clase Usuario
        if ($follow == null || get_class($follow) != "Follow") {
            return false;
        }

        $id = $follow->getId();
        
        $sql = "DELETE from follows where id = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("i", $id);
        $stmt->execute();
        $result = $stmt->get_result();

        // affected_rows comprueba si se ha borrado 1 línea
        if ($this->conn->affected_rows > 0) {
            return true;
        } else {
            return false;
        }
    }

    /**
     * Borra el follow de la BD
     * @param type $follow Follow a borrar
     * @return true si se ha borrado bien o false o si no se ha borrado
     */
    public function deleteByFollower($follow) {
        // Comprobamos que el parámetro no es nulo y si es de la clase Usuario
        if ($follow == null || get_class($follow) != "Follow") {
            return false;
        }

        $id_user_follower = $follow->getUser_id_follower();
        $id_user_followed = $follow->getUser_id_followed();
        
        $sql = "DELETE from follows where user_id_follower = ? and user_id_followed = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("ii", $id_user_follower, $id_user_followed);
        $stmt->execute();
        $result = $stmt->get_result();

        // affected_rows comprueba si se ha borrado 1 línea
        return ($this->conn->affected_rows > 0);
    }

    public function findByFollowedUsers($id) {
        if (!is_int($id)) {
            return false;
        }

        $sql = "SELECT * from follows where user_id_follower = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("i", $id);

        $stmt->execute();
        $result = $stmt->get_result();

        $array_follows = array();
        while ($follow = $result->fetch_object("Follow")) {
            $array_follows[] = $follow;
        }
        
        return $array_follows;
    }

    public function isFollowing($follow) {
        /*if (!$follow instanceof Follow) {
            return false;
        }*/

        $id_user_follower = $follow->getUser_id_follower();
        $id_user_followed = $follow->getUser_id_followed();

        $sql = "SELECT * from follows where user_id_follower = ? and user_id_followed = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("ii", $id_user_follower, $id_user_followed);

        $stmt->execute();
        $result = $stmt->get_result();

        return ($result->num_rows > 0);
    }
}
