from django.urls import path
from .views import home_view, explore_view, sessions_view, community_list_view, topic_delete_view, community_room_view, public_profile_view

urlpatterns = [
    path('home/', home_view, name='home'),
    path('explore/', explore_view, name='explore'),
    path('sessions/', sessions_view, name='sessions'),
    path('community/', community_list_view, name='community'),
    path('community/delete/<uuid:topic_id>/', topic_delete_view, name='topic_delete'),
    path('community/room/<uuid:topic_id>/', community_room_view, name='community_room'),
    path('profile/<uuid:pp_id>/', public_profile_view, name='public_profile'),
]
