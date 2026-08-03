from django.urls import path
from . import views

urlpatterns = [
    path("chat/<uuid:user_id>/", views.chat, name="chat"),
]