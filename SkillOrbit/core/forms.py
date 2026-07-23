from django import forms
from .models import Topic, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            'title',
            'description'
            ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Give your topic a clear title...',
                'class': 'topic-input-field'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'What should we discuss in this topic room?',
                'rows': 3,
                'class': 'topic-textarea-field'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'COMMENT HERE',
                'rows' : 2,
                'class': 'chat-textarea-field'
            })
        }