import re
import string

from crispy_forms.bootstrap import InlineField, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, HTML, Field
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.exceptions import ValidationError, EmptyResultSet
from django.db.models import Q
from django.forms.models import inlineformset_factory
from django.forms.widgets import Input
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

# from nekomon.models import User
from django.conf.urls.static import static
from six import b

from nekomon.models import User, Post, Follow

REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class LogInForm(forms.Form):
    username = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "input-text",
                'placeholder': _("Username"),
            }
        )
    )

    password = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': "input-text",
                'placeholder': _("Password"),
            }
        )
    )

    class Meta:
        model = User
        exclude = [
            'created_at',
            'last_modified_at',
            'email',
            'profile_picture',
            'name',
            'description',
            'cookie_id',
            'registration_ip',
        ]

    # Validations
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        is_validated = True

        if len(username) == 0:
            self.add_error(None, ValidationError(_("The username field cannot be empty.")))
            is_validated = False
        elif len(username) > 15:
            self.add_error(None, ValidationError(_("The username field characters has exceeded.")))
            is_validated = False

        if len(password) == 0:
            self.add_error(None, ValidationError(_("The password field cannot be empty.")))
            is_validated = False
        elif len(password) > 15:
            self.add_error(None, ValidationError(_("The username field characters has exceeded.")))
            is_validated = False

        if is_validated:
            user = authenticate(
                username=username,
                password=password,
            )

            if user is None:
                self.add_error(None, ValidationError(
                    _("The introduced username was not found or does not match with the password."))
                )

        # is_validated = True
        # if username is None:
        #     self.add_error(field=None, error=ValidationError("The username field cannot be empty."))
        #     is_validated = False
        # elif len(username) > 15:
        #     self.add_error(field=None, error=ValidationError("The username field characters has exceeded."))
        #     is_validated = False
        #
        # if password is None:
        #     self.add_error(field=None, error=ValidationError("The password field cannot be empty."))
        #     is_validated = False
        # elif len(password) > 60:
        #     self.add_error(field=None, error=ValidationError("The password field characters has exceeded."))
        #     is_validated = False

        # try:
        #     User.objects.get(
        #         username=username,
        #         password=password,
        #     )
        # except User.DoesNotExist as dne:
        #     self.add_error(field=None, error=ValidationError(
        #         "The username was not found or does not match with the password.")
        #     )


class RegisterForm(forms.Form):
    email = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "input-text",
                'placeholder': _("E-mail"),
            }
        )
    )

    username = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "input-text",
                'placeholder': _("Username"),
            }
        )
    )

    password = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': "input-text",
                'placeholder': _("Password"),
            }
        )
    )

    repeat_password = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': "input-text",
                'placeholder': _("Repeat the password"),
            }
        )
    )

    class Meta:
        # model = User
        exclude = [
            'created_at',
            'last_modified_at',
            'profile_picture',
            'name',
            'description',
            'cookie_id',
            'registration_ip',
        ]

    # Validations
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        cleaned_data['username'] = strip_tags(cleaned_data.get('username'))
        username = cleaned_data.get('username')
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        is_validated = True

        if len(email) == 0:
            self.add_error(None, ValidationError(_("The e-mail field cannot be empty.")))
            is_validated = False
        elif len(email) > 40:
            self.add_error(None, ValidationError(_("The e-mail field characters has exceeded.")))
            is_validated = False
        elif not re.fullmatch(REGEX, email):
            self.add_error(None, ValidationError(_("The e-mail format is incorrect.")))
            is_validated = False

        if len(username) == 0:
            self.add_error(None, ValidationError(_("The username field cannot be empty.")))
            is_validated = False
        elif len(username) > 15:
            self.add_error(None, ValidationError(_("The username field characters has exceeded.")))
            is_validated = False
        elif username is not username.replace(" ", ""):
            self.add_error(None, ValidationError(_("The username must not contain space characters.")))
            is_validated = False

        if len(password) == 0:
            self.add_error(None, ValidationError(_("The password field cannot be empty.")))
            is_validated = False
        elif len(password) > 15:
            self.add_error(None, ValidationError(_("The username field characters has exceeded.")))
            is_validated = False
        elif password != repeat_password:
            self.add_error(None, ValidationError(_("The introduced passwords do not match.")))
            is_validated = False

        if is_validated:
            try:
                User.objects.get(
                    Q(email=email) | Q(username=username),
                )

                self.add_error(None, ValidationError(_("An account with the introduced e-mail or username already exists.")))
            except User.DoesNotExist as dne:
                # self.save()

                User.objects.create(
                    email=email,
                    username=username,
                    password=make_password(password),
                    profile_picture='qn0eoAq',
                    name=username,
                    # get_ip_address(request)
                )


class UpdateUserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UpdateUserForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        max_length=25,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "input-user-text",
                #"value": request.user.name,
                'placeholder': _("Name"),
            }
        )
    )

    username = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "input-user-text",
                'placeholder': _("Username"),
            }
        )
    )

    description = forms.CharField(
        max_length=140,
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': "input-user-description",
                'placeholder': _("Description"),
            }
        )
    )

    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'style': "display: none",
            }
        )
    )

    class Meta:
        # model = User
        exclude = [
            'created_at',
            'last_modified_at',
            'password',
            'last_login',
            'description',
            'email',
            'registration_ip',
            'date_joined',
            'profile_header_image',
        ]

    # Validations
    def clean(self):
        cleaned_data = super().clean()

        cleaned_data["username"] = strip_tags(cleaned_data.get('username'))
        username = cleaned_data.get('username')

        cleaned_data["name"] = strip_tags(cleaned_data.get('name'))
        name = cleaned_data.get('name')

        description = cleaned_data.get('description')

        print(cleaned_data)

        is_validated = True

        # if len(username) == 0:
        #     self.add_error(None, ValidationError(_("The username field cannot be empty.")))
        #     is_validated = False
        if len(username) > 15:
            self.add_error(None, ValidationError(_("The username field characters has exceeded.")))
            is_validated = False
        elif username is not username.replace(" ", ""):
            self.add_error(None, ValidationError(_("The username must not contain space characters.")))
            is_validated = False

        elif len(name) > 25:
            self.add_error(None, ValidationError(_("The name field characters has exceeded.")))
            is_validated = False

        elif len(description) > 140:
            self.add_error(None, ValidationError(_("The description field characters has exceeded.")))
            is_validated = False

        if is_validated:
            try:
                user = User.objects.get(
                    username=username,
                )

                if self.request.user.id != user.id:
                    self.add_error(None, ValidationError(_("An account with the introduced username already exists.")))
            except User.DoesNotExist as dne:
                pass
                # self.save()

                # user = self.request.user
                #
                # User.objects.update(
                #     username=username,
                #     name=name,
                #     description=description,
                # )


class PostForm(forms.Form):

    content = forms.CharField(
        max_length=140,
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': "new-post-content",
                'placeholder': _("New post"),
            }
        )
    )

    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'style': "display: none",
            }
        )
    )

    in_response_to = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                'style': "display: none",
            }
        )
    )

    # Validations
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['content'] = strip_tags(cleaned_data.get('content'))

        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        in_response_to = cleaned_data.get("in_response_to")

        if in_response_to == "undefined" or in_response_to == "":
            in_response_to = None

        # If an image is uploaded there is no need for content
        if image is None and len(content) == 0:
            self.add_error(None, ValidationError(_("The content of the post cannot be empty.")))
        elif len(content) > 140:
            self.add_error(None, ValidationError(_("The content of the post characters has exceeded.")))

        if in_response_to is not None:
            try:
                Post.objects.get(
                    id=in_response_to,
                )
            except Post.DoesNotExist:
                self.add_error(None, ValidationError(_("The post you've tried to reply to was not found.")))


class FollowUnfollowForm(forms.Form):
    user_id = forms.CharField(
        max_length=140,
        required=False,
        widget=forms.HiddenInput(
            attrs={
                # 'value': "{{profile.id}}",
            }
        )
    )

    is_following = forms.CharField(
        max_length=5,
        required=False,
        widget=forms.HiddenInput(
            attrs={
                # 'value': "{{is_following}}",
            }
        )
    )

    # Validations
    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get("user_id")
        is_following = cleaned_data.get("is_following")

        if is_following == "True":
            is_following = bool(True)
        else:
            is_following = bool("")

        cleaned_data['is_following'] = is_following

        if len(str(user_id)) == 0:
            self.add_error(None, ValidationError(_("Cannot be empty.")))
        if len(str(is_following)) == 0:
            self.add_error(None, ValidationError(_("Cannot be empty.")))
        else:
            try:
                user = User.objects.get(
                    id=user_id
                )
            except User.DoesNotExist as dne:
                self.add_error(None, ValidationError(_("User not found.")))


class LikePostForm(forms.Form):
    post_id = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.HiddenInput(
            attrs={
                # 'value': "{{profile.id}}",
            }
        )
    )

    # is_already_liked = forms.CharField(
    #     max_length=5,
    #     required=False,
    #     widget=forms.HiddenInput(
    #         attrs={
    #             # 'value': "{{is_following}}",
    #         }
    #     )
    # )

    # Validations
    def clean(self):
        cleaned_data = super().clean()

        post_id = cleaned_data.get("post_id")
        # is_following = cleaned_data.get("is_following")
        #
        # if is_following == "True":
        #     is_following = bool(True)
        # else:
        #     is_following = bool("")
        #
        # cleaned_data['is_following'] = is_following

        if len(str(post_id)) == 0:
            self.add_error(None, ValidationError(_("Cannot be empty.")))
        # if len(str(is_following)) == 0:
        #     self.add_error(None, ValidationError(_("Cannot be empty.")))
        else:
            try:
                Post.objects.get(
                    id=post_id
                )
            except Post.DoesNotExist:
                self.add_error(None, ValidationError(_("Post not found.")))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': "input-text",
                'placeholder': _("E-mail"),
            }
        )
    )

    class Meta:
        model = User
        exclude = [
            'created_at',
            'last_modified_at',
            'email',
            'profile_picture',
            'name',
            'description',
            'cookie_id',
            'registration_ip',
            'password',
        ]

    # Validations
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        is_validated = True

        if len(email) == 0:
            self.add_error('email', ValidationError(_("The e-mail field cannot be empty.")))
            is_validated = False
        elif len(email) > 40:
            self.add_error('email', ValidationError(_("The e-mail field characters has exceeded.")))
            is_validated = False
        elif not re.fullmatch(REGEX, email):
            self.add_error('email', ValidationError(_("The e-mail format is incorrect.")))
            is_validated = False

        if is_validated:
            try:
                user = User.objects.get(
                    email=email,
                )

                # password = password.encode()
                # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
                #
                # if not bcrypt.checkpw(password, user.password.encode()):
                #     self.add_error(None, ValidationError(
                #         _("The introduced password does not match with the username."))
                #     )
                # else:
                #     print("Coincide")

            except User.DoesNotExist as dne:
                self.add_error(None, ValidationError(
                    _("An account registered by that e-mail was not found."))
                )


class CustomPasswordSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': "input-text",
                'placeholder': _("Password"),
            }
        )
    )

    new_password2 = forms.CharField(
        max_length=60,
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': "input-text",
                'placeholder': _("Repeat the password"),
            }
        )
    )

    class Meta:
        model = User
        exclude = [
            'created_at',
            'last_modified_at',
            'email',
            'profile_picture',
            'name',
            'description',
            'cookie_id',
            'registration_ip',
            'username',
        ]

    # Validations
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password1")
        repeat_password = cleaned_data.get("new_password2")

        is_validated = True

        if len(password) == 0:
            self.add_error(None, ValidationError(_("The password field cannot be empty.")))
            is_validated = False
        elif len(password) > 15:
            self.add_error(None, ValidationError(_("The username field characters has exceeded.")))
            is_validated = False
        elif password != repeat_password:
            self.add_error(None, ValidationError(_("The introduced passwords do not match.")))
            is_validated = False

        # if is_validated:
        #     try:
        #         user = User.objects.get(
        #             email=email,
        #         )
        #
        #         # password = password.encode()
        #         # hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        #         #
        #         # if not bcrypt.checkpw(password, user.password.encode()):
        #         #     self.add_error(None, ValidationError(
        #         #         _("The introduced password does not match with the username."))
        #         #     )
        #         # else:
        #         #     print("Coincide")
        #
        #     except User.DoesNotExist as dne:
        #         self.add_error(None, ValidationError(
        #             _("An account registered by that e-mail was not found."))
        #         )