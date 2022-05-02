from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:page>/<str:username>/', consumers.PostConsumer.as_asgi()),
]
