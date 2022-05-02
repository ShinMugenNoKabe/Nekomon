import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import close_old_connections

from nekomon.models import Follow, User


class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.page = self.scope['url_route']['kwargs']['page']
        self.username = self.scope['url_route']['kwargs']['username']

        user = await get_user(self.username)

        if user is not None:
            self.my_group = 'group_%s' % user.id

            # Join group of user that you follow
            await self.channel_layer.group_add(
                self.my_group,
                self.channel_name
            )

            if self.page == "feed":
                follows = await get_followed_users(user)

                if follows is not None:
                    for follow in follows:
                        # Join group of users that you follow
                        self.user_followed = 'group_%s' % follow.user_followed_id

                        await self.channel_layer.group_add(
                            self.user_followed,
                            self.channel_name
                        )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.my_group,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        post = text_data_json['post']

        await self.channel_layer.group_send(
            self.my_group,
            {
                'type': 'sent_post',
                'new_post': post
            }
        )

    # Receive message from group
    async def sent_post(self, event):
        new_post = event['new_post']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'new_post': new_post
        }))


@database_sync_to_async
def get_user(username):
    close_old_connections()
    try:
        user = User.objects.get(
            username=username
        )

        return user
    except ObjectDoesNotExist:
        return None


@database_sync_to_async
def get_followed_users(user):
    close_old_connections()
    try:
        follows = Follow.objects.filter(
            user_follower_id=user.id
        )

        if len(follows) > 0:
            return follows
        else:
            return None
    except ObjectDoesNotExist:
        return None
