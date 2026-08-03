from django import forms
from django.utils import timezone
from .models import ScheduleSession

class ScheduleSessionForm(forms.ModelForm):
    class Meta:
        model = ScheduleSession
        fields = ['name', 'description', 'time_scheduled', 'meeting_link']
        widgets = {
            'time_scheduled': forms.DateTimeInput(attrs={
                'type': 'text',
                'class': 'form-control custom-picker-trigger',
                'placeholder': 'Click to select Date & Time...',
                'readonly': 'readonly',
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Title (e.g. Django Pair Programming)',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Session details...',
                'rows': 3,
                'class': 'form-control'
            }),
            'meeting_link': forms.URLInput(attrs={
                'placeholder': 'https://meet.google.com/meeting (Optional)',
                'class': 'form-control'
            })
        }

    def clean_time_scheduled(self):
        time_scheduled = self.cleaned_data.get('time_scheduled')
        if time_scheduled and time_scheduled < timezone.now():
            raise forms.ValidationError("Select time and date forward, don't choose the past time and date field.")
        return time_scheduled
