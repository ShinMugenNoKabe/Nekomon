import base64
import json
import ast
import os
from datetime import datetime, timedelta

import requests

from base64 import b64encode

from django.forms.utils import ErrorDict
from django.http import JsonResponse
from django.template.backends import django

from nekomon.exceptions import UploadImageToImgurException

from django.utils.translation import gettext_lazy as _
import timeago

from dotenv import load_dotenv

from nekomon.models import Post

load_dotenv()


def build_post_in_html(post):
    formatted_post_date = post.created_at.strftime("%Y-%m-%d %H:%M:%S")

    post_html = "<div class='post'>"

    # Header
    post_html +=    "<div class='post-header'>"
    post_html +=        "<div>"
    post_html +=            "<img class='post-pfp' src='/web/images/profile_pictures/" + post.user.profile_picture + "'/>"
    post_html +=        "</div>"
    post_html +=        "<div class='post-username-date'>"
    post_html +=            "<a href='/" + post.user.username + "'>"
    post_html +=                "<p>" + post.user.name + "</p>"
    post_html +=                "<p>@" + post.user.username + "</p>"
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
        post_html +=    "<hr>"
        post_html +=    "<div class='post-content'>" + post.content + "</div>"

    post_html +=    "<hr>"

    if post.image != "":
        post_html +=        "<div class='post-image'>"
        post_html +=            "<img src='https://i.imgur.com/" + post.image + ".png' alt='" +\
                                    _("Image attached to the post") + "'>"
        post_html +=        "</div>"
        post_html +=        "<hr>"

    post_html +=    "<i class='fas fa-heart'></i>"

    post_html += "</div>"

    return post_html


def build_multiple_posts_in_html(posts):
    posts_html = ""

    for post in posts:
        posts_html += build_post_in_html(post)

    return posts_html


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def upload_image_to_imgur(request):
    client_id = os.getenv("IMGUR_CLIENT_ID")

    headers = {"Authorization": "Client-ID " + client_id}

    api_key = os.getenv("IMGUR_API_KEY")

    url = "https://api.imgur.com/3/upload.json"

    image = request.FILES.get("image")

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
        return data_response.get("id")
    else:
        error = data_response.get("error")

        if error == "File is over the size limit":
            raise UploadImageToImgurException(_("The image is too big."))


def return_errors(object_error):
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
    return Post.objects.raw(
        "SELECT * FROM nekomon_post ORDER BY RAND() LIMIT 1"
    )[0]
