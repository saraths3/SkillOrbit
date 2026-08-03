from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.ScheduleSessionView, name='schedule_session'),
    path('schedule/<uuid:user_id>/', views.ScheduleSessionView, name='schedule_session_with_user'),
    path('accept/<int:session_id>/', views.accept_session_view, name='accept_session'),
    path('complete/<int:session_id>/', views.complete_session_view, name='complete_session'),
    path('cancel/<int:session_id>/', views.cancel_session_view, name='cancel_session'),
]