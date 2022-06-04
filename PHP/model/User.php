<?php

class User {

    private $id;
    private $email;
    private $username;
    private $password;
    private $registration_date;
    private $profile_picture;
    private $name;
    private $description;
    private $cookie_id;
    private $registration_ip;

    private $posts;
    private $followed_users_posts;
    private $followers;
    private $followed_users;

    function getId() {
        return $this->id;
    }

    function getEmail() {
        return $this->email;
    }
    
    function getUsername() {
        return $this->username;
    }

    function getPassword() {
        return $this->password;
    }

    function getRegistration_date() {
        $phpdate = strtotime($this->registration_date);
        $mysqldate = date('d/m/Y ', $phpdate);

        return $mysqldate;
    }

    function getProfile_picture() {
        return $this->profile_picture;
    }

    function getRegistration_ip() {
        return $this->registration_ip;
    }

    function getName() {
        return $this->name;
    }

    function getDescription() {
        return $this->description;
    }

    function setId($id): void {
        $this->id = $id;
    }

    function setRegistration_ip($registration_ip): void {
        $this->registration_ip = $registration_ip;
    }

    function setEmail($email): void {
        $this->email = $email;
    }

    function setUsername($username): void {
        $this->username = $username;
    }

    function setPassword($password): void {
        $this->password = $password;
    }

    function setProfile_picture($profile_picture): void {
        $this->profile_picture = $profile_picture;
    }

    function setRegistration_date($registration_date): void {
        $this->registration_date = $registration_date;
    }

    function setName($name): void {
        $this->name = $name;
    }

    function setDescription($description): void {
        $this->description = $description;
    }

    function getCookie_id() {
        return $this->cookie_id;
    }

    function setCookie_id($cookie_id): void {
        $this->cookie_id = $cookie_id;
    }

    function getPosts($conn) {
        if (!isset($this->posts)) {
            $postDAO = new PostDAO($conn);
            $this->posts = $postDAO->findByUserId($this->getId());
        }
        
        return $this->posts;
    }

    function setPosts($posts): void {
        $this->posts = $posts;
    }

    function getFollowerd_users_posts($conn) {
        if (!isset($this->posts)) {
            $postDAO = new PostDAO($conn);
            $this->posts = $postDAO->findByFollowedUsers($this->getId());
        }
        
        return $this->posts;
    }

    function setFollowerd_users_posts($followerd_users_posts): void {
        $this->followerd_users_posts = $followerd_users_posts;
    }

    function getFollowers() {
        return $this->followers;
    }

    function setFollowers($followers): void {
        $this->followers = $followers;
    }

    function getFollowed_users($conn) {
        if (!isset($this->followed_users)) {
            $folDAO = new FollowDAO($conn);
            $this->followed_users = $folDAO->findByFollowedUsers($this->getId());
        }

        return $this->followed_users;
    }

    function setFollowed_users($followed_users): void {
        $this->followed_users = $followed_users;
    }

    function isFollowing($conn, $user_id_followed) {
        $folDAO = new FollowDAO($conn);
        $follow = new Follow();
        $follow->setUser_id_follower($this->getId());
        $follow->setUser_id_followed($user_id_followed);

        return $folDAO->isFollowing($follow);
    }
    
}
