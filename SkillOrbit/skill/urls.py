from django.urls import path
from .views import add_skills, delete_skills, edit_skills, skill_request, All_Skill_Requests, My_Skill_Requests, My_Connection

urlpatterns = [
    path('add/', add_skills, name='add_skills'),
    path('delete/<int:sid>/', delete_skills, name='delete_skill'),
    path('edit/<int:sid>/', edit_skills, name='edit_skills'),
    path('profile/request/', skill_request, name='skill_request'),
    path('requests/', All_Skill_Requests, name='all_skill_requests'),
    path('myrequests/' , My_Skill_Requests, name='my_requests'),
    path('connections/', My_Connection, name='my_connections')
]