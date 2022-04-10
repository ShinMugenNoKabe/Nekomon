"""nekomon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from nekomon.forms import CustomPasswordResetForm, CustomPasswordSetPasswordForm
from nekomon.views.api_views import api_get_username
from nekomon.views.views import go_to_main_view, log_in_ajax, register_ajax, logout_view, user_profile_view, \
    new_post_ajax, \
    list_posts_main_ajax, \
    list_posts_profile_ajax, post_view, log_in_view, register_view, follow_unfollow_ajax, testimage
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main
    path('', go_to_main_view, name='main_view'),

    # Login
    path('login/', log_in_view, name='log_in_view'),
    path('ajax/login/', log_in_ajax, name='log_in_ajax'),

    # Logout
    path('logout/', logout_view, name='logout_view'),

    # Reset password
    # path('pw-reset/', auth_views.password_reset, name='password_reset_view'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
            form_class=CustomPasswordResetForm,
            template_name="user_forms/password_reset/reset_form.html",
        ),
        name='password_reset',
    ),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name="user_forms/password_reset/reset_email_sent.html",
        ),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
            form_class=CustomPasswordSetPasswordForm,
            template_name="user_forms/password_reset/reset_new_password.html",
        ),
        name='password_reset_confirm'
    ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="user_forms/password_reset/reset_done.html",
    ), name='password_reset_complete'),

    # Register
    path('register/', register_view, name='register_view'),
    path('ajax/new-account/', register_ajax, name='new_account_ajax'),

    # User profile
    path('<str:profile>', user_profile_view, name='user_profile_view'),

    # Posts
    path('posts/<int:pk>', post_view, name='post_view'),
    path('ajax/new-post/', new_post_ajax, name='new_post_ajax'),
    path('ajax/list-posts-main/', list_posts_main_ajax, name='list_posts_main_ajax'),
    path('ajax/list-posts-profile/<int:pk>', list_posts_profile_ajax, name='list_posts_profile_ajax'),
    
    # Follows / unfollows
    path('ajax/follow-unfollow/', follow_unfollow_ajax, name='follow_unfollow_ajax'),

    # NekoBot API
    path('api/user/<str:username>', api_get_username, name='api_get_username'),

    path('testimage', testimage, name='testimage'),
]
