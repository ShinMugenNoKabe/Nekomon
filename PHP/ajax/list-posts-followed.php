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
        $postDAO = new PostDAO($conn);
        $posts = $postDAO->findByFollowedUsers(Session::obtain_id());

        $json = array();

        $linksPattern = '~[a-z]+://\S+~';
        $usersPattern = '~@+[a-zA-Z0-9]+~';
        $youtubePattern = '~src=~+youtube.com\/watch\?v=+[a-zA-Z0-9]+~';
        
        foreach ($posts as $post) {
            // Links
            if (preg_match_all($linksPattern, $post->getContent(), $out)) {
                foreach ($out[0] as $link) {
                    $newContent = str_replace($link,"<a target='_blank' href='$link'>$link</a>", $post->getContent());
                    $post->setContent($newContent);
                }
            }
            
            // User mentions
            if (preg_match_all($usersPattern, $post->getContent(), $out)) {
                foreach ($out[0] as $userFound) {
                    $userFound = substr($userFound, 1);
                    if ($userMentioned = $usuDAO->findByUsername($userFound)) {
                        $newContent = str_replace(("@" . $userFound),"<a target='_blank' href='https://nekomon.es/$userFound'>@$userFound</a>", $post->getContent());
                        $post->setContent($newContent);
                    }
                }
            }

            // Youtube Videos
            if (preg_match_all($youtubePattern, $post->getContent(), $out)) {
                foreach ($out[0] as $video) {
                    $videoID = substr($video, 20);
                    $post->setContent($post->getContent() . "<br>
                        <iframe width='420' height='315'
                            src='https://www.youtube.com/embed/$videoID'>
                        </iframe>"
                    );
                }
            }

            // Youtube Videos
            /*if (str_contains($post->getContent(), "https://www.youtube.com/watch?v=")) {
                $youtubePosition = strpos($post->getContent(),'https://www.youtube.com/watch?v=');
                $videoID = substr($post->getContent(), $youtubePosition);
                parse_str(parse_url($videoID, PHP_URL_QUERY), $my_array_of_vars); 

                $videoID = ('https://www.youtube.com/embed/' . $my_array_of_vars['v']);

                $post->setContent($post->getContent() . "<br>
                    <iframe width='420' height='315'
                    src='$videoID'>
                    </iframe>"
                );
            }*/

            $json[] = array(
                "content" => $post->getContent(),
                "date" => $post->getDate(),
                "username" => $post->getUser()->getUsername(),
                "name" => $post->getUser()->getName(),
                "profile_picture" => $post->getUser()->getProfile_picture()
            );
        }

        $jsonString = json_encode($json);
        print($jsonString);
    } else {
        //FlashMessages::addMessage("error-not-logged-in", "Debe de iniciar sesión para continuar.");

        header("Location: https://www.nekomon.es/");
    }