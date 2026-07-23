from django.contrib import admin

# Register your models here.
from .models import Skill, UserSkill, SkillRequest, Connection

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'proficiency', 'years_of_experience')
    search_fields = ('user__username', 'skill__name')
    ordering = ('user', 'skill')

@admin.register(SkillRequest)
class SkillRequestAdmin(admin.ModelAdmin):
    ordering = ('skill',)

admin.site.register(Connection)