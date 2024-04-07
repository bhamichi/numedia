from django.contrib import admin

from .models.project import Participants, Project

# Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'icon', 'name', 'key', 'description', 'lead', 'created_at')

@admin.register(Participants)
class ParticipantsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'project', 'joined_at')