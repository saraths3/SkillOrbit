from django.db import models

# Create your models here.

import uuid
from django.conf import settings

class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=100, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='My_Topics')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='My_Comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self',null=True, blank=True, on_delete=models.CASCADE, related_name='replies' )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'commented by {self.user.username}, {self.user.email}'