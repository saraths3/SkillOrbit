from django.db import models
from django.conf import settings

class Course(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=False, help_text="Required YouTube tutorial URL.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        author = self.user.username if self.user else "Anonymous"
        return f"{self.title} (@{author})"

    @property
    def video_id(self):
        url = self.video_url
        if 'watch?v=' in url:
            return url.split('watch?v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            return url.split('youtu.be/')[1].split('?')[0]
        elif 'embed/' in url:
            return url.split('embed/')[1].split('?')[0]
        return ""

    @property
    def thumbnail_url(self):
        if self.video_id:
            return f"https://img.youtube.com/vi/{self.video_id}/hqdefault.jpg"
        return ""

    @property
    def embed_url(self):
        if self.video_id:
            return f"https://www.youtube.com/embed/{self.video_id}"
        return ""