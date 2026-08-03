from django import forms
from .models import ScheduleSession

class ScheduleSessionForm(forms.ModelForm):
    class Meta():
        model = ScheduleSession
        fields = ['name', 'description', 'meeting_link', 'time_scheduled']
        widgets = {
            'time_scheduled': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Title',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Description',
                'rows': 3,
                'class': 'form-control'
            }),
            'meeting_link': forms.URLInput(attrs={
                'placeholder': 'https://meet.google.com/meeting (Optional)',
                'class': 'form-control'
            })
        }
