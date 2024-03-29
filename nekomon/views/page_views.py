"""
Request page views
"""

from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from nekomon.exceptions import UploadImageToImgurException
from nekomon.forms import LogInForm, RegisterForm, PostForm, FollowUnfollowForm, UpdateUserForm, LikePostForm
from nekomon.models import User, Post, Follow, Like
from nekomon.utils import upload_image_to_imgur, return_errors, build_multiple_posts_in_html, \
    build_post_in_html, get_random_post
from django.utils.translation import gettext_lazy as _


@login_required
def go_to_main_view(request):
    """Goes to the main feed page"""
    
    posts = Post.objects.raw(
        "SELECT distinct nekomon_post.* from nekomon_post, nekomon_follow" +
        " where (user_follower_id = " + str(request.user.id) + " and nekomon_post.user_id = user_followed_id)" +
        " or nekomon_post.user_id = " + str(request.user.id) +
        " and in_response_to_id is null " +
        " order by created_at desc"
    )

    if len(posts) == 0:
        posts = Post.objects.raw(
            "SELECT distinct nekomon_post.* from nekomon_post" +
            " where nekomon_post.user_id = " + str(request.user.id) +
            " and in_response_to_id is null " +
            " order by created_at desc"
        )

    random_post = get_random_post()

    if random_post is not None:
        random_post = build_post_in_html(random_post)

    context = {
        "posts": build_multiple_posts_in_html(posts),
        "random_post": random_post,
        "post_box": PostForm,
        "update_form": UpdateUserForm,
    }

    return render(request, 'main_site.html', context)


def user_profile_view(request, profile):
    """Goes to the user profile view"""

    try:
        profile = User.objects.get(
            username=profile
        )
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse_lazy('main_view'))
    
    follow = Follow.objects.filter(
        user_followed_id=profile.id,
        user_follower_id=request.user.id,
    )
        
    is_following = len(follow) > 0

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
        "user_is_viewing_their_profile": profile.username == request.user.username,
    }

    return render(request, 'user_profile.html', context)


def post_view(request, pk):
    """Goes to the post view"""

    try:
        post = Post.objects.get(
            id=pk
        )

        name = post.user.name

        in_response_to_post = post.in_response_to

        previous_posts_list = []
        previous_posts = ""

        while in_response_to_post is not None:
            previous_posts_list.append(in_response_to_post)
            in_response_to_post = in_response_to_post.in_response_to

        if len(previous_posts_list) > 0:
            previous_posts_list.reverse()

            for previous_post in previous_posts_list:
                previous_posts += build_post_in_html(previous_post)
                previous_posts += "<hr>"

        post = build_post_in_html(post)

        replies = Post.objects.filter(
            in_response_to=pk
        ).order_by("created_at")

        if len(replies) > 0:
            replies = build_multiple_posts_in_html(replies)
            post += "<hr>"
    except ObjectDoesNotExist:
        return go_to_main_view()

    random_post = get_random_post()

    post_form = PostForm(initial={"in_response_to": pk})
        
    context = {
        "name": name,
        "is_viewing_post": True,
        "previous_posts": previous_posts,
        "post": post,
        "id_post": pk,
        "replies": replies,
        "random_post": build_post_in_html(random_post),
        "update_form": UpdateUserForm,
        "post_box": post_form,
        "in_response_to": pk
    }

    return render(request, 'post_view.html', context)


def log_in_view(request):
    """Goes to the log in view if the user is not logged in"""
    
    if request.user.is_authenticated:
        return go_to_main_view(request)
    
    context = {
        'form': LogInForm,
    }

    return render(request, 'user_forms/user_login.html', context)


def logout_view(request):
    """Logouts the session"""

    logout(request)
    return HttpResponseRedirect(reverse('log_in_view'))


def register_view(request):
    """Goes to the register view if the user is not logged in"""
    
    if request.user.is_authenticated:
        return go_to_main_view(request)
    
    context = {
        'form': RegisterForm
    }

    return render(request, 'user_forms/user_register.html', context)


def search_users(request):
    """Looks for users on the database"""

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

