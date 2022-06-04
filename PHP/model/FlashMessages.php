<?php

/**
 * Description of FlashMessages
 *
 * @author DAW2
 */
class FlashMessages {

    private $json;
    
    public function __construct() {
        $this->json = array();
    }

    public function addMessage($type, $message) {
        $this->json[] = array(
            /* "error_message" => $message */
            $type => $message
        );
    }

    public function showMessages() {
        return $this->json;
    }

}
