from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.core import serializers
from nekomon.models import User
import json


def api_get_username(request, username):
    if request.method == "GET":

        try:
            user = User.objects.get(
                username=username
            )

            serialized_user = serializers.serialize('json', [user], fields=(
                'username',
                'profile_picture',
                'date_joined',
                'name',
                'description',
            ))

            return JsonResponse({"user": json.loads(serialized_user)})
        except ObjectDoesNotExist:
            return JsonResponse({"user": None})
    else:
        response = JsonResponse({"message": "Not found"})
        response.status_code = 403  # To announce that the user isn't allowed to publish

        return response