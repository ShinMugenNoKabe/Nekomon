"""
Views used by the API (Discord Bot)
"""

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.decorators import api_view
from nekomon.models import User, Post
from nekomon.views.serializers import UserSerializer, PostSerializer


@api_view(["GET"])
def api_get_username(request, username):
    """Returns a serialized user for the given username"""
    
    try:
        user = User.objects.get(
            username=username
        )

        serialized_user = UserSerializer(user)

        return JsonResponse({"user": serialized_user.data})
    except ObjectDoesNotExist:
        return JsonResponse({"user": None})


@api_view(["GET"])
def api_get_post(request, post_id):
    """Returns a serialized post for the given id"""
    
    try:
        post = Post.objects.get(
            id=post_id
        )

        serialized_post = PostSerializer(post)

        return JsonResponse({"post": serialized_post.data})
    except ObjectDoesNotExist:
        return JsonResponse({"post": None})