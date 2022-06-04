<?php

class Post {

    private $id;
    private $user_id;
    private $content;
    private $date;

    private $user;
    private $likes;

    function getId() {
        return $this->id;
    }

    function getUser_id() {
        return $this->user_id;
    }
    
    function getContent() {
        return $this->content;
    }

    function getDate() {
        $phpdate = strtotime($this->date);
        $mysqldate = date('d/m/Y H:i:s', $phpdate);

        return $mysqldate;
    }

    function setId($id): void {
        $this->id = $id;
    }

    function setUser_id($user_id): void {
        $this->user_id = $user_id;
    }

    function setContent($content): void {
        $this->content = $content;
    }

    function setDate($date): void {
        $this->date = $date;
    }

    function getUser() {
        if (!isset($this->user)) {
            $userDAO = new UserDAO(SQLDBConnection::connect());
            $this->user = $userDAO->find($this->getUser_id());
        }
        
        return $this->user;
    }

    function getLikes() {
        return $this->content;
    }

    function setLikes($likes): void {
        $this->likes = $likes;
    }

}
