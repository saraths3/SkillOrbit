from django import forms
from .models import UserSkill, SkillRequest

class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ('skill', 'proficiency', 'years_of_experience')


class SkillRequestForm(forms.ModelForm):
    class Meta:
        model = SkillRequest
        fields = ('skill', 'message')