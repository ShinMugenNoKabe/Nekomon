from django.contrib import admin
# from nekomon.models import User
from django.template.defaultfilters import linebreaksbr
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from nekomon.models import User, Post, Follow


class UserAdmin(admin.ModelAdmin):
    """Admin List View"""
    list_display = ("id", "username", "email", "name", "profile_picture", "description", "registration_ip")
    list_filter = ("id", )

    exclude = ("password", )

    search_fields = ["email", 'username', 'name', 'registration_ip']


class PostAdmin(admin.ModelAdmin):
    """Post List View"""
    list_display = ("id", "user_id", "created_at", "content", "image", "in_response_to_id")
    list_filter = ("id", )

    def user_id(self, obj):
        return format_html("<a href='{url}'>{username}</a>",
                           url="/admin/nekomon/user/" + str(obj.user.id),
                           username=obj.user.username)

    def in_response_to_id(self, obj):
        return format_html("<a href='{url}'>{id}</a>",
                           url="/admin/nekomon/post/" + str(obj.in_response_to_id),
                           id=str(obj.in_response_to_id))

    search_fields = ["content", 'user_id__username', "in_response_to_id__id"]


class FollowAdmin(admin.ModelAdmin):
    """Follow List View"""
    list_display = ("id", "created_at", "user_followed_id", "user_follower_id")

    def user_followed_id(self, obj):
        return format_html("<a href='{url}'>{username}</a>",
                           url="/admin/nekomon/user/" + str(obj.user_followed.id),
                           username=obj.user_followed.username)

    def user_follower_id(self, obj):
        return format_html("<a href='{url}'>{username}</a>",
                           url="/admin/nekomon/user/" + str(obj.user_follower.id),
                           username=obj.user_follower.username)

    list_filter = ("id", )

    search_fields = ['user_followed_id__username', "user_follower_id__username"]


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow, FollowAdmin)
