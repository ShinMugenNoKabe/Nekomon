from django.urls import path

from nekomon import consumers

websocket_urlpatterns = [
    # Feed and user view
    path('ws/<str:page>/<str:username>/', consumers.PostConsumer.as_asgi()),

    # Post view
    path('ws/post/<int:post>', consumers.PostViewConsumer.as_asgi()),
]
