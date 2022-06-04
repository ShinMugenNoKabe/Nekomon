<?php

include("Post.php");

class PostDAO {

    private $conn;
    
    public function __construct($conn) {
        $this->conn = $conn;
    }
        
    /**
     * Devuelve el post de la BD
     * @param type $id ID del post
     * @return \Post Post o null si no existe
     */
    public function find($id): Post {
        if (!is_int($id)) {
            return false;
        }

        $sql = "SELECT * from posts where id = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("i", $id);

        $stmt->execute();
        $result = $stmt->get_result();

        // fetch_object() devuelve un objeto de una clase
        return $result->fetch_object("Post");
    }

    /**
     * Devuelve todos los posts de la BD
     * @param type $column Campo de la BD por el que se van a ordenar
     * @param type $order Tipo de orden (ASC o DESC)
     * @return array Array de objetos de la clase Post
     */
    public function findAll($column = "id", $order = "ASC"): Array {
        if (!is_string($column) || !is_order($order)) {
            return false;
        }

        $sql = "SELECT * from posts order by ? ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("ss", $column, $order);

        $stmt->execute();
        $result = $stmt->get_result();

        // fetch_object() devuelve un objeto de una clase
        return $result->find_all(0, $this->conn->fetch_object("Post"));
    }

    /**
     * Inserta el post en la BD
     * @param type $post Post a insertar
     * @return true si se ha insertado bien o false o si no se ha insertado
     */
    public function insert($post) {
        if (!$post instanceof Post) {
            return false;
        }

        $user_id = $post->getUser_id();
        $content = $post->getContent();
        
        $sql = "INSERT into posts (user_id, content) VALUES (?, ?)";

        $stmt = $this->conn->prepare($sql);
        $stmt->bind_param("is", $user_id, $content);

        $stmt->execute();

        // Guarda el id que se le ha asignado la base de datos al objeto en la variable $id
        $post->setId($this->conn->insert_id);

        return true;
    }
    
    /**
     * Actualiza el post de la BD
     * @param type $post Post a actualizar
     * @return true si se ha actualizado bien o false o si no se ha actualizado
     */
    public function update($post) {
        if (!$user instanceof Post) {
            return false;
        }

        $id = $post->getId();
        $user_id = $post->getUser_id();
        $content = $post->getContent();

        $sql = "UPDATE posts set "
            . "user_id = ?, content = ? "
            . "where id = ?";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("isi", $user_id, $content, $id);
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
     * Borra el post de la BD
     * @param type $post Post a borrar
     * @return true si se ha borrado bien o false o si no se ha borrado
     */
    public function delete($post) {
        // Comprobamos que el parámetro no es nulo y si es de la clase Usuario
        if ($post == null || get_class($post) != "Post") {
            return false;
        }

        $id = $post->getId();
        
        $sql = "DELETE from posts where id = ? ";

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
     * Devuelve todos los posts de la BD según su id de usuario
     * @param type $user_id id del usuario
     * @return array Array de objetos de la clase Post
     */
    public function findByUserId($user_id) {
        if (!is_int($user_id)) {
            return false;
        }

        $sql = "SELECT * from posts where user_id = ? order by date desc";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("i", $user_id);

        $stmt->execute();
        $result = $stmt->get_result();

        $array_posts = array();
        while ($post = $result->fetch_object("Post")) {
            $array_posts[] = $post;
        }
        
        return $array_posts;
    }

    /**
     * Devuelve todos los posts de la BD según los follows del usuario
     * @param type $user_id id del usuario
     * @return array Array de objetos de la clase Post
     */
    public function findByFollowedUsers($user_id) {
        if (!is_int($user_id)) {
            return false;
        }

        $sql = "SELECT distinct posts.* from posts, follows where user_id_follower = ? and posts.user_id = user_id_followed or posts.user_id = ? order by date desc";

        if (!$stmt = $this->conn->prepare($sql)) {
            die("Error al preparar la consulta: " . $this->conn->error);
        }

        $stmt->bind_param("ii", $user_id, $user_id);

        $stmt->execute();
        $result = $stmt->get_result();

        $array_posts = array();
        while ($post = $result->fetch_object("Post")) {
            $array_posts[] = $post;
        }
        
        return $array_posts;
    }
}