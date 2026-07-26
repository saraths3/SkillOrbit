from django.urls import path
from .views import chat

urlpatterns = [
    path('chat/<uuid:user_id>', chat, name='chat')
]