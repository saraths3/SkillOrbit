from django.urls import path
from .views import *

urlpatterns = [
    path('signin/',signin_view ,name='signin'),
    path('signup/', signup_view,name='signup'),
    path('signout/', signout_view, name='signout'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', edit_profile_view, name = 'edit_profile'),
    path('forgotpassword/', forgot_password_view, name='forgot_password'),
    path('resetpassword/', reset_password_view, name='reset_password'),
]