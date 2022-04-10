import base64
import json
import ast
import requests

from base64 import b64encode


def upload_image_to_imgur(request):
    client_id = '2f491d6a2d5cc9d'

    headers = {"Authorization": "Client-ID 2f491d6a2d5cc9d"}

    api_key = 'caebd7e369f6fdbd884b77232a7df5130d0836d1'

    url = "https://api.imgur.com/3/upload.json"

    image = request.FILES.get("image")

    #print("LECTURA: " + image.read())

    # print("NOMBRE: " + image)

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

    content = response.content.decode("utf-8")
    json_response = json.loads(content)

    return json_response.get("data").get("id")


def image_upload_location(instance, filename):
    return "media/beer/images/%s.png" % (instance.id)


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
