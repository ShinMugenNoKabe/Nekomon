import base64
import json
import ast
import requests

from base64 import b64encode

from django.forms.utils import ErrorDict
from django.http import JsonResponse
from django.template.backends import django

from nekomon.exceptions import UploadImageToImgurException

from django.utils.translation import gettext_lazy as _


def upload_image_to_imgur(request):
    client_id = '2f491d6a2d5cc9d'

    headers = {"Authorization": "Client-ID " + client_id}

    api_key = 'caebd7e369f6fdbd884b77232a7df5130d0836d1'

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

    data_response = json_response.get("data")
    is_success = json_response.get("success")

    if is_success:
        return data_response.get("id")
    else:
        error = data_response.get("error")

        if error == "File is over the size limit":
            raise UploadImageToImgurException(_("The image is too big."))


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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
