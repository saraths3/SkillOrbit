from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class User_RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        full_name = forms.CharField(max_length = 100)
        email = forms.EmailField()
        model = CustomUser
        fields = (
            'full_name',
            'username',
            'email',
        )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'avatar',
            'full_name',
            'bio',
            'headline',
            'github_url',
            'linkedin_url',
            'career_level',
        )
        