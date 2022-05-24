import pdb

import bcrypt
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
import json
from django.conf import settings

# Create your views here.
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, CreateView

from nekomon.exceptions import UploadImageToImgurException
from nekomon.forms import LogInForm, RegisterForm, PostForm, FollowUnfollowForm, UpdateUserForm, LikePostForm
# from nekomon.models import User
from nekomon.models import User, Post, Follow, Like
from nekomon.utils import get_ip_address, upload_image_to_imgur, return_errors, build_multiple_posts_in_html, \
    build_post_in_html, get_random_post
from django.utils.translation import gettext_lazy as _


@login_required
def go_to_main_view(request):
    posts = Post.objects.raw(
        "SELECT distinct nekomon_post.* from nekomon_post, nekomon_follow where user_follower_id = "
        + str(request.user.id) +
        " and in_response_to_id is null " +
        " and nekomon_post.user_id = user_followed_id or nekomon_post.user_id = " + str(request.user.id) +
        " order by created_at desc"
    )

    random_post = get_random_post()
    
    context = {
        "posts": build_multiple_posts_in_html(posts),
        "random_post": build_post_in_html(random_post),
        "post_box": PostForm,
        "update_form": UpdateUserForm,
    }

    return render(request, 'main_site.html', context)


def user_profile_view(request, profile):
    try:
        profile = User.objects.get(
            username=profile
        )
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse_lazy('main_view'))
    
    follow = None
    
    try:
        follow = Follow.objects.get(
            user_followed_id=profile.id,
            user_follower_id=request.user.id,
        )
        
        is_following = True
    except ObjectDoesNotExist:
        is_following = False

    posts = Post.objects.raw(
        "SELECT distinct nekomon_post.* from nekomon_post where user_id = " + str(profile.id) +
        " and in_response_to_id is null " +
        " order by created_at desc"
    )

    random_post = get_random_post()

    context = {
        "profile": profile,
        "posts": build_multiple_posts_in_html(posts),
        "post_box": PostForm,
        "is_following": is_following,
        "follow_unfollow_form": FollowUnfollowForm(
            initial={
                'user_id': profile.id,
                'is_following': is_following,
            },
        ),
        "random_post": build_post_in_html(random_post),
        "update_form": UpdateUserForm,
    }

    return render(request, 'user_profile.html', context)


def post_view(request, pk):
    try:
        post = Post.objects.get(
            id=pk
        )

        name = post.user.name

        post = build_post_in_html(post)

        replies = Post.objects.filter(
            in_response_to=pk
        ).order_by("created_at")

        replies = build_multiple_posts_in_html(replies)
    except ObjectDoesNotExist:
        return go_to_main_view()

    random_post = get_random_post()

    post_form = PostForm(initial={"in_response_to": pk})
        
    context = {
        "name": name,
        "is_viewing_post": True,
        "post": post,
        "replies": replies,
        "random_post": build_post_in_html(random_post),
        "update_form": UpdateUserForm,
        "post_box": post_form,
        "in_response_to": pk
    }

    return render(request, 'post_view.html', context)


def log_in_view(request):
    if request.user.is_authenticated:
        return go_to_main_view(request)
    else:
        context = {
            'form': LogInForm,
        }

        return render(request, 'user_forms/user_login.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return go_to_main_view(request)
    else:
        context = {
            'form': RegisterForm
        }

        return render(request, 'user_forms/user_register.html', context)


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
        if user is not None:
            login(request, user)
            return go_to_main_view(request)
            # return HttpResponseRedirect(reverse_lazy('main_view'))
            # return render(request, "calender.html")
        else:
            print("test")


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

        if user is not None:
            user.registration_ip = get_ip_address(request)
            user.save()

            login(request, user)
            return go_to_main_view(request)
            # return HttpResponseRedirect(reverse_lazy('main_view'))
            # return render(request, "calender.html")
        else:
            print("test")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('log_in_view'))


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
            #content = ""

            try:
                image = upload_image_to_imgur(request, "image")
            except UploadImageToImgurException as ex:
                return return_errors(str(ex))

        if in_response_to != "":
            post_in_response_to = Post.objects.get(
                id=in_response_to
            )

        post = Post.objects.create(
            content=content,
            user_id=request.user.id,
            image=image,
            in_response_to=post_in_response_to
        )

        # Post.save()

        response = JsonResponse({"post": build_post_in_html(post)})
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
            # Post.save()

            response.status_code = 200
            return response


@login_required
def update_profile(request):
    if request.method == "POST":
        form = UpdateUserForm(request.POST, request.FILES, request=request)

        if not form.is_valid():
            return return_errors(form.errors)

        new_username = form.cleaned_data['username']
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']

        user = request.user

        old_username = user.username

        profile_picture = ""

        if user is not None:

            if request.FILES:
                try:
                    profile_picture = upload_image_to_imgur(request, "profile_picture")
                    user.profile_picture = profile_picture
                except UploadImageToImgurException as ex:
                    return return_errors(str(ex))
            else:
                profile_picture = user.profile_picture

            if new_username != "":
                user.username = new_username
            else:
                new_username = old_username

            if name != "":
                user.name = name
            else:
                name = user.name

            if description != "":
                user.description = description
            else:
                description = user.description

            if profile_picture != "":
                user.profile_picture = profile_picture

            user.save()
            update_session_auth_hash(request, user)

            response = JsonResponse({
                    "old_username": old_username,
                    "new_username": new_username,
                    "name": name,
                    "description": description,
                    "profile_picture": profile_picture
            })
            response.status_code = 200
            return response
        else:
            print("No action")


@csrf_exempt
def search_users(request):
    if request.method == "POST":

        print(request)

        input = request.POST.get("input")

        try:
            found_users = User.objects.filter(
                Q(username__contains=input) | Q(name__contains=input)
            )

            data = serializers.serialize('json', found_users)
            response = HttpResponse(data, content_type="application/json")
            response.status_code = 200
            return response
        except ObjectDoesNotExist:
            print("test")

