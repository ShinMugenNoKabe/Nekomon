<?php
    session_start();

    require ("../model/SQLDBConnection.php");
    require ("../model/FlashMessages.php");
    require ("../model/UserDAO.php");
    require ("../model/PostDAO.php");
    require ("../model/Session.php");

    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        $conn = SQLDBConnection::connect();

        $usuDAO = new UserDAO($conn);
        $user = $usuDAO->findByUsername(Session::getRequestedUserName());
        $posts = $user->getPosts($conn);

        $json = array();

        $linksPattern = "~[a-z]+://\S+~";
        $usersPattern = '~@+[a-zA-Z0-9]+~';
        $youtubePattern = '~src=~+youtube.com\/watch\?v=+[a-zA-Z0-9]+~';
        
        foreach ($posts as $post) {
            // Links
            if ($linksFound = preg_match_all($linksPattern, $post->getContent(), $url)) {
                $newContent = $post->getContent();
                $links = Array();

                foreach ($url[0] as $link) {
                    if (count($url[0]) !== count(array_unique($url[0]))) {
                        $links[] = $link;

                        $newContent = str_replace($link, ("<a target='_blank' href='" . $link ."'>" . $link . "</a>"), $post->getContent());
                    } else {
                        $newContent .= "Test ";
                    }
                    
                }

                $post->setContent($newContent);
            }
            
            // User mentions
            if (preg_match_all($usersPattern, $post->getContent(), $out)) {
                foreach ($out[0] as $userFound) {
                    $userFound = substr($userFound, 1);

                    if ($userMentioned = $usuDAO->findByUsername($userFound)) {
                        $newContent = str_replace(("@" . $userFound),"<a target='_blank' href='https://nekomon.es/$userFound'>@$userFound</a>", $post->getContent());
                    }

                    $post->setContent($newContent);
                }
            }

            // Youtube Videos
            /*if (preg_match_all($youtubePattern, $post->getContent(), $out)) {
                foreach ($out[0] as $video) {
                    $videoID = substr($video, 20);

                    $post->setContent($post->getContent() . "<br>
                        <iframe width='420' height='315'
                            src='https://www.youtube.com/embed/$videoID'>
                        </iframe>"
                    );
                }
            }*/

            $json[] = array(
                "content" => $post->getContent(),
                "date" => $post->getDate(),
                "username" => $post->getUser()->getUsername(),
                "name" => $post->getUser()->getName(),
                "profile_picture" => $post->getUser()->getProfile_picture(),
                //"likesCount" => count($post->getLikes())
            );
        }

        $jsonString = json_encode($json);
        print($jsonString);
    } else {
        //FlashMessages::addMessage("error-not-logged-in", "Debe de iniciar sesión para continuar.");

        header("Location: https://www.nekomon.es/");
    }