"""
ASGI config for nekomon project.
It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
import django

from nekomon.consumers import PostViewConsumer, PostConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nekomon.settings")
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter([
            # Feed and user view
            path('ws/<str:page>/<str:username>/', PostConsumer.as_asgi()),

            # Post view
            path('ws/post/id/<int:post>/', PostViewConsumer.as_asgi()),
        ])
    ),
})