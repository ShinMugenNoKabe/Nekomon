<?php

class Follow {

    private $id;
    private $user_id_followed;
    private $user_id_follower;

    function getId() {
        return $this->id;
    }

    function getUser_id_followed() {
        return $this->user_id_followed;
    }
    
    function getUser_id_follower() {
        return $this->user_id_follower;
    }

    function setId($id): void {
        $this->id = $id;
    }

    function setUser_id_followed($user_id_followed): void {
        $this->user_id_followed = $user_id_followed;
    }

    function setUser_id_follower($user_id_follower): void {
        $this->user_id_follower = $user_id_follower;
    }
    
}
