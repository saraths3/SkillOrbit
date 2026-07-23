from django.db import models
from django.conf import settings


# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return self.name
    
class UserSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    PROFICIENCY_LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert')
    ]
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_LEVEL, default='beginner')
    years_of_experience = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Skill'
        verbose_name_plural = 'Users Skills'
        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'skill'],
                name = 'unique_user_skill'
            )]

    def __str__(self):
        return f'{self.user.username}: {self.skill.name}'

class SkillRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    STATUS = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Skill Request'
        verbose_name_plural = 'Skill Requests'
    
    def __str__(self):
        return f'request from {self.from_user.username} to {self.to_user.username}'
    
class Connection(models.Model):
    user_one = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='connection1')
    user_two = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='connection2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Connection'
        verbose_name_plural ='Connections'
        constraints = [
            models.UniqueConstraint(
                fields= ['user_one', 'user_two'],
                name= 'unique_connection'
            )
        ]
    
    def __str__(self):
        return f'{self.user_one} connected to {self.user_two}'