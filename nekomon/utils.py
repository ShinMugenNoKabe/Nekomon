"""
Utils methods container
"""

import json
import os
import requests
from base64 import b64encode
from django.forms.utils import ErrorDict
from django.http import JsonResponse
from nekomon.exceptions import UploadImageToImgurException
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
from nekomon.models import Post, User
import re


load_dotenv()


def build_post_in_html(post):
    """Builds a given post to HTML"""
    
    replies = Post.objects.filter(
        in_response_to=post
    ).count()

    if post.in_response_to is not None:
        post_html = "<div class='post' id='post-" + str(post.id) + "'>"
    else:
        post_html = "<div class='post'>"

    # Header
    post_html +=    "<div class='post-header'>"
    post_html +=        "<div>"
    post_html +=            "<img class='post-pfp' data-pfp='" + post.user.username + "' src='https://i.imgur.com/" + post.user.profile_picture + ".jpg' alt='" + post.user.username + "profile picture' />"
    post_html +=        "</div>"
    post_html +=        "<div class='post-username-date'>"
    post_html +=            "<a data-username-link='" + post.user.username + "' href='/" + post.user.username + "'>"
    post_html +=                "<p data-name='" + post.user.username + "'>" + post.user.name + "</p>"
    post_html +=                "<p data-username='" + post.user.username + "'>@" + post.user.username + "</p>"
    post_html +=            "</a>"
    post_html +=            "<p>"
    post_html +=                "<a href='/posts/" + str(post.id) + "'>"
    post_html +=                    "<time class='timeago' datetime='" + post.created_at.isoformat() + "'>"
    post_html +=                        post.created_at.strftime("%d of %B, %Y at %I:%M:%S %p")
    post_html +=                    "</time>"
    post_html +=                "</a>"
    post_html +=            "</p>"
    post_html +=        "</div>"
    post_html +=    "</div>"

    # Content
    if post.content != "":
        content = process_content(post.content)
        post_html +=    "<hr>"
        post_html +=    "<div class='post-content'>" + content + "</div>"
        alt_message = post.content
    else:
        alt_message = _("Image attached to the post")

    post_html +=    "<hr>"

    if post.image != "":
        post_html +=        "<div class='post-image'>"
        post_html +=            "<img src='https://i.imgur.com/" + post.image + ".jpg' alt='" + alt_message + "'>"
        post_html +=        "</div>"
        post_html +=        "<hr>"

    post_html +=    "<a href='/posts/" + str(post.id) + "' target='_blank'><i class='fa-solid fa-reply'></i>"
    post_html +=    "<span class='post-replies-counter' data-post-replies='" + str(post.id) + "'>" + str(replies) + "</span>"
    post_html +=    "</a>"
    #post_html +=    "<i class='fas fa-heart like-post-icon' data-like-id='" + str(post.id) + "' ></i>"

    post_html += "</div>"

    return post_html


def build_multiple_posts_in_html(posts):
    """Builds a list of posts to HTML"""
    
    posts_html = ""

    for post in posts:
        posts_html += build_post_in_html(post)

    return posts_html


def process_content(content):
    """Processes a post content to add user mentions, links and youtube embeds"""
    
    # Users
    users_in_content = list(set(re.findall("@[a-zA-Z0-9]+", content)))

    if len(users_in_content) > 0:
        for at_username in users_in_content:
            username = at_username[1:]

            user = User.objects.filter(
                username=username
            )

            if len(user) > 0:
                content = content.replace(at_username, "<a target='_blank' href='/" + user[0].username + "'>@" + user[0].username + "</a>&nbsp;")

    # URLs and YouTube videos
    youtube_videos_in_content = list(set(re.findall(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})', content)))

    if len(youtube_videos_in_content) > 0:
        video = youtube_videos_in_content[0]
        video_id = video[-1]
        video_url = (video[0] + video[1] + video[2] + "." + video[3] + "/" + video[4] + video_id)

        content = content.replace(
            video_url,
            "<iframe width='560' height='315' src='https://www.youtube.com/embed/" + video_id + "' title='YouTube video player'"
            "frameborder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'"
            "allowfullscreen></iframe>"
        )

    urls_in_content = list(set(re.findall(r'(https?://[^\s]+)', content)))

    if len(urls_in_content) > 0:
        for url in urls_in_content:
            if url.find("https://www.youtube.com/embed/") == -1:
                content = content.replace(url, "<a target='_blank' href='" + url + "'>" + url + "</a>&nbsp;")

    return content


def get_ip_address(request):
    """Gets the user's IP address"""
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def upload_image_to_imgur(request, name):
    """Uploads an image to Imgur"""
    
    client_id = os.getenv("IMGUR_CLIENT_ID")

    headers = {"Authorization": "Client-ID " + client_id}

    api_key = os.getenv("IMGUR_API_KEY")

    url = "https://api.imgur.com/3/upload.json"

    image = request.FILES.get(name)

    response = requests.post(
        url,
        headers=headers,
        data={
            'key': api_key,
            'image': b64encode(image.read()),
            'type': 'base64',
            'name': 'image',
            'title': 'Nekomon image'
        }
    )

    json_response = json.loads(response.content.decode("utf-8"))

    print(json_response)

    data_response = json_response.get("data")
    is_success = json_response.get("success")

    if is_success:
        image.close()
        return data_response.get("id")
    else:
        error = data_response.get("error")
        print(type(error))
        
        error_message = ""
        
        if type(error) is str:
            error_message = error
        else:
            error_message = error.get("message")
            
        raise UploadImageToImgurException(error_message)


def return_errors(object_error):
    """Returns client errors as JSON"""
    
    list_errors = []

    if type(object_error) is ErrorDict:

        for errors, error in object_error.items():
            list_errors.append(error)

    else:
        list_errors.append(object_error)

    response = JsonResponse({"error": list_errors})
    response.status_code = 403  # To announce that the user isn't allowed to publish

    return response


def get_random_post():
    """Gets a random post from the database"""
    
    random_post = Post.objects.raw(
        "SELECT * FROM nekomon_post ORDER BY RAND() LIMIT 1"
    )[0]
    
    return random_post
