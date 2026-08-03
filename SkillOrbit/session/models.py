from django.db import models
from django.conf import settings
# Create your models here.
class ScheduleSession(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='session_host')
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_scheduled =models.DateTimeField()
    STATUS = {
        'accepted': 'Accepted',
        'pending': 'Pending',
        'complete': 'Complete',
        'canceled': 'Canceled',
    }
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    meeting_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.status}'