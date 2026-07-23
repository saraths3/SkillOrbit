from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email','username')
    search_fields = ('email', 'full_name', 'username')
    
    list_display = ('username','email')

    fieldsets = [
        ('Personal Info', {
            'fields': ('full_name',)
        }),
        ('Credentials', {
            'fields': ('username','email'),
        }),
        ('Important Data', {
            'fields': ('last_login','is_staff', 'is_superuser', 'created_at')
        }),

    ]

admin.site.register(CustomUser, CustomAdmin)
admin.site.register(UserProfile)