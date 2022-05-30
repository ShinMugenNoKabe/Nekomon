from django.contrib.auth.models import AbstractUser
from django.db import models

from nekomon import settings
from core.models import CommonInfo
from django.utils.timezone import now


# Create your models here.
class User(AbstractUser):
    profile_picture = models.CharField("Profile picture", max_length=200)
    name = models.CharField("Name", max_length=150)
    description = models.CharField("Description", max_length=200)
    registration_ip = models.CharField("Registration IP", max_length=20)

    # Metadatos
    class Meta:
        # Nombre que muestra de la clase
        verbose_name = "User"
        verbose_name_plural = "Users"

        # Orden de la lista
        # ordering = ["name"]
        # Orden descendente
        ordering = ["username"]

    def __str__(self):
        return self.username


class Post(CommonInfo):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="posts",
        on_delete=models.CASCADE,
    )

    content = models.CharField("Content", max_length=500)

    image = models.CharField(max_length=10)

    in_response_to = models.ForeignKey(
        "self",
        related_name="replies",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    # Metadatos
    class Meta:
        # Nombre que muestra de la clase
        verbose_name = "Post"
        verbose_name_plural = "Posts"

        # Orden de la lista
        # Orden descendente
        ordering = ["-id"]

    def __str__(self):
        return str(self.id)


class Follow(CommonInfo):
    user_follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="follower",
        on_delete=models.CASCADE,
        default=0,
        unique=False,
    )

    user_followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="followed",
        on_delete=models.CASCADE,
        default=0,
        unique=False,
    )

    # Metadatos
    class Meta:
        # Nombre que muestra de la clase
        verbose_name = "Follow"
        verbose_name_plural = "Follows"

        # Orden de la lista
        # ordering = ["name"]
        # Orden descendente
        ordering = ["-id"]

    def __str__(self):
        return "Follower: " + str(self.user_follower.id) + ", followed: " + str(self.user_followed.id)


class Like(CommonInfo):
    user_liker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="liker",
        on_delete=models.CASCADE,
        default=0,
        unique=False,
    )

    post_liked = models.ForeignKey(
        Post,
        related_name="post",
        on_delete=models.CASCADE,
        default=0,
        unique=False,
    )

    class Meta:
        verbose_name = "Like"
        verbose_name_plural = "Likes"

        ordering = ["id"]

    # def __str__(self):
    #     return str(self.id)
