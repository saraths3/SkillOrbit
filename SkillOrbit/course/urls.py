from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list_view, name='course_list'),
    path('create/', views.create_course_view, name='create_course'),
]