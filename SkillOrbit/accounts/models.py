from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.utils import timezone


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password = None,**extra_fields):
        if not email: raise ValueError('Error: Provide Email')
        user_email = self.normalize_email(email)
        user = self.model(email=user_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password =None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email, password,**extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username =models.CharField(max_length=100, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='accounts/avatar', blank=True)
    headline = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    EXPERIENCE_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    career_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='beginner')
    
    def __str__(self):
        return f"{self.user.username} ({self.user.email})"