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
            'headline',
            'bio',
            'career_level',
            'github_url',
            'linkedin_url',
        )
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sarath S'}),
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Full Stack Developer | Python & Django'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your developer journey and learning goals...'}),
            'career_level': forms.Select(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/username'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/username'}),
        }
        