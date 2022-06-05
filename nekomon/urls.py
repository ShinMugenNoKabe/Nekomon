"""
URLs patterns configuration
"""
from django.contrib import admin
from django.urls import path

from nekomon.forms import CustomPasswordResetForm, CustomPasswordSetPasswordForm
from nekomon.views.ajax_views import follow_unfollow_ajax, like_post_ajax, log_in_ajax, new_post_ajax, register_ajax
from nekomon.views.api_views import api_get_username, api_get_post
from nekomon.views.page_views import go_to_main_view, logout_view, user_profile_view, \
    log_in_view, register_view, post_view, update_profile, search_users
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main view
    path('', go_to_main_view, name='main_view'),

    # Login
    path('login/', log_in_view, name='log_in_view'),
    path('ajax/login/', log_in_ajax, name='log_in_ajax'),

    # Logout
    path('logout/', logout_view, name='logout_view'),

    # Reset password
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
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
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

    # Update profile
    path('ajax/update-profile/', update_profile, name='update_profile'),

    # User profile
    path('<str:profile>', user_profile_view, name='user_profile_view'),

    # Posts
    path('posts/<int:pk>', post_view, name='post_view'),
    path('ajax/new-post/', new_post_ajax, name='new_post_ajax'),
    path('ajax/like-post/', like_post_ajax, name='like_post_ajax'),

    # Follows / unfollows
    path('ajax/follow-unfollow/', follow_unfollow_ajax, name='follow_unfollow_ajax'),

    # User search
    path('ajax/search-users/', search_users, name='search_users'),

    # API views
    path('api/user/<str:username>', api_get_username, name='api_get_username'),
    path('api/post/<int:post_id>', api_get_post, name='api_get_post'),
]

handler404 = "nekomon.views.handlers_views.handler404"
handler500 = "nekomon.views.handlers_views.handler500"
