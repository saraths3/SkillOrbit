from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    video_url = forms.URLField(
        required=True,
        error_messages={
            'required': 'A valid YouTube video link is required to publish a course.'
        },
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.youtube.com/watch?v=... (Required YouTube Link)',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'video_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Course Title (e.g. Intro to Python & Django)',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Explain what viewers will learn in this video...',
                'rows': 3,
                'class': 'form-control'
            }),
        }

    def clean_video_url(self):
        url = self.cleaned_data.get('video_url', '').strip()
        if not url:
            raise forms.ValidationError("A YouTube video link is required to publish a course.")
        return url