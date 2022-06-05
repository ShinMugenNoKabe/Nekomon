"""
AJAX petitions
"""

from django.http import JsonResponse
from nekomon.exceptions import UploadImageToImgurException
from nekomon.forms import FollowUnfollowForm, LikePostForm, LogInForm, PostForm, RegisterForm
from nekomon.models import Follow, Post
from nekomon.utils import build_post_in_html, get_ip_address, return_errors, upload_image_to_imgur
from django.contrib.auth import authenticate, login
from nekomon.views.page_views import go_to_main_view


def log_in_ajax(request):
    if request.method == "POST":
        form = LogInForm(request.POST or None)

        if not form.is_valid():
            return return_errors(form.errors)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        
        user = authenticate(
            username=username,
            password=password,
        )
        
        login(request, user)
        return go_to_main_view(request)


def register_ajax(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if not form.is_valid():
            return return_errors(form.errors)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(
            username=username,
            password=password,
        )

        user.registration_ip = get_ip_address(request)
        user.save()

        login(request, user)
        return go_to_main_view(request)
    
    
def new_post_ajax(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if not form.is_valid():
            return return_errors(form.errors)

        content = form.cleaned_data['content']
        in_response_to = form.cleaned_data['in_response_to']

        image = ""

        post_in_response_to = None

        if request.FILES:
            try:
                image = upload_image_to_imgur(request, "image")
            except UploadImageToImgurException as ex:
                return return_errors(str(ex))

        if in_response_to != "" and in_response_to != "undefined":
            post_in_response_to = Post.objects.get(
                id=in_response_to
            )

        post = Post.objects.create(
            content=content,
            user_id=request.user.id,
            image=image,
            in_response_to=post_in_response_to
        )

        response = JsonResponse({
            "post": build_post_in_html(post),
            "post_id": str(in_response_to)
        })

        response.status_code = 200
        return response


def like_post_ajax(request):
    if request.method == "POST":
        form = LikePostForm(request.POST or None)

        if not form.is_valid():
            return return_errors(form.errors)

        post_id = form.cleaned_data['post_id']

        like = Like(
            user_liker_id=request.user.id,
            post_liked_id=post_id,
        )

        like.save()

        response = JsonResponse("True", safe=False)
        # Post.save()

        response.status_code = 200
        return response


def follow_unfollow_ajax(request):
    if request.method == "POST":
        form = FollowUnfollowForm(request.POST or None)

        if not form.is_valid():
            return return_errors(form.errors)

        user_id = form.cleaned_data['user_id']
        is_following = form.cleaned_data['is_following']

        if not str(user_id) == str(request.user.id):
            if is_following:
                follow = Follow.objects.get(
                    user_followed_id=user_id,
                    user_follower_id=request.user.id,
                )

                follow.delete()

                response = JsonResponse("False", safe=False)
            else:
                follow = Follow(
                    user_followed_id=user_id,
                    user_follower_id=request.user.id,
                )

                follow.save()

                response = JsonResponse("True", safe=False)

            response.status_code = 200
            return response
        