import pdb

import bcrypt
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import authenticate, login, logout
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

from nekomon.forms import LogInForm, RegisterForm, PostForm, FollowUnfollowForm
# from nekomon.models import User
from nekomon.models import User, Post, Follow
from nekomon.utils import get_ip_address


@login_required
def go_to_main_view(request):
    random_post = Post.objects.raw(
        "SELECT * FROM nekomon_post ORDER BY RAND() LIMIT 1"
    )
    
    context = {
        'post_box': PostForm,
        'random_post': random_post[0]
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

    context = {
        "profile": profile,
        'post_box': PostForm,
        'is_following': is_following,
        'follow_unfollow_form': FollowUnfollowForm(
            initial={
                'user_id': profile.id,
                'is_following': is_following,
            },
        ),
    }

    return render(request, 'user_profile.html', context)


def post_view(request, pk):
    try:
        post = Post.objects.get(
            id=pk
        )
    except ObjectDoesNotExist:
        return go_to_main_view()
        
    context = {
        "post": post,
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

        if form.is_valid():
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
        else:
            response = JsonResponse({"errors": form.errors.as_json()})
            response.status_code = 403  # To announce that the user isn't allowed to publish

            # response.status_code = 403  # To announce that the user isn't allowed to publish
            return response


def register_ajax(request):
    if request.method == "POST":
        form = RegisterForm(request.POST or None)

        if form.is_valid():
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

        else:
            response = JsonResponse({"errors": form.errors.as_json()})
            response.status_code = 403  # To announce that the user isn't allowed to publish

            # response.status_code = 403  # To announce that the user isn't allowed to publish
            return response


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('log_in_view'))


def new_post_ajax(request):
    if request.method == "POST":
        form = PostForm(request.POST or None)

        if form.is_valid():
            content = form.cleaned_data['content']

            Post.objects.create(
                content=content,
                user_id=request.user.id,
            )
            # Post.save()
            response = JsonResponse("test", safe=False)
            response.status_code = 200
            return response
        else:
            list_errors = []
            for errors, error in form.errors.items():
                list_errors.append(error)

            response = JsonResponse({"error": list_errors})
            response.status_code = 403  # To announce that the user isn't allowed to publish

            # response.status_code = 403  # To announce that the user isn't allowed to publish
            return response


def follow_unfollow_ajax(request):
    if request.method == "POST":
        form = FollowUnfollowForm(request.POST or None)

        if form.is_valid():
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
        else:
            list_errors = []
            for errors, error in form.errors.items():
                list_errors.append(error)

            response = JsonResponse({"error": list_errors})
            response.status_code = 403  # To announce that the user isn't allowed to publish

            # response.status_code = 403  # To announce that the user isn't allowed to publish
            return response


@csrf_exempt
def list_posts_main_ajax(request):
    if request.method == "POST":
        posts = Post.objects.raw(
            "SELECT distinct nekomon_post.* from nekomon_post, nekomon_follow where user_follower_id = "
            + str(request.user.id) +
            " and nekomon_post.user_id = user_followed_id or nekomon_post.user_id = " + str(request.user.id) +
            " order by created_at desc"
        )

        posts_json = []

        for post in posts:
            user = User.objects.get(
                id=post.user_id,
            )

            post_dict = {
                'id': str(post.id),
                'created_at': str(post.created_at),
                'last_modified_at': str(post.created_at),
                'content': post.content,
                'user': {
                    'username': user.username,
                    'name': user.name,
                    'profile_picture': user.profile_picture
                }
            }

            posts_json.append(post_dict)

        response = JsonResponse(posts_json, safe=False)
        response.status_code = 200
        return response
    else:
        pass


@csrf_exempt
def list_posts_profile_ajax(request, pk):
    if request.method == "POST":
        posts = Post.objects.raw(
            "SELECT distinct nekomon_post.* from nekomon_post where user_id = " + str(pk) +
            " order by created_at desc"
        )

        posts_json = []

        for post in posts:
            user = User.objects.get(
                id=post.user_id,
            )

            post_dict = {
                'id': str(post.id),
                'created_at': str(post.created_at),
                'last_modified_at': str(post.created_at),
                'content': post.content,
                'user': {
                        'username': user.username,
                        'name': user.name,
                        'profile_picture': user.profile_picture
                    }
                }

            posts_json.append(post_dict)

        response = JsonResponse(posts_json, safe=False)
        print(posts_json)
        response.status_code = 200
        return response
    else:
        pass
        # list_errors = []
        # for errors, error in posts.errors.items():
        #     list_errors.append(error)
        #
        # response = JsonResponse({"error": list_errors})
        # response.status_code = 403  # To announce that the user isn't allowed to publish
        #
        # # response.status_code = 403  # To announce that the user isn't allowed to publish
        # return response
        # else:
        #     list_errors = []
        #     for errors, error in form.errors.items():
        #         list_errors.append(error)
        #
        #     response = JsonResponse({"error": list_errors})
        #     response.status_code = 403  # To announce that the user isn't allowed to publish
        #
        #     # response.status_code = 403  # To announce that the user isn't allowed to publish
        #     return response



