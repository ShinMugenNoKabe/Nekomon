<?php
$linksPattern = "~[a-z]+://\S+~";
$content = "https://www.nekomon.es/rufino https://www.nekomon.es/rufino https://www.nekomon.es/rufino https://www.nekomon.es/rufino https://www.nekomon.";
if ($linksFound = preg_match_all($linksPattern, $content, $url)) {
                $newContent = $content;

                /*if (in_array($url[0], $os)) {
                    echo "Existe Irix";
                }*/

                //foreach ($url[0] as $url) {
                    print_r("$url[0]:" . count($url[0]) !== count(array_unique($url[0])));
                //}

                

            /*foreach ($url[0] as $link) {
                    $newContent = str_replace($link, ("<a target='_blank' href='" . $link ."'>" . $link . "</a>"), $post->getContent());
            }

                $post->setContent($newContent);*/
            }
            ?>