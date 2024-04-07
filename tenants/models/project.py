"""
clean is a method provided by Django to perform custom validation at the model level.
We can perform any checks on the model data before it saved to the database. 
If a validation error is detected, you can raise a ValidationError 
to prevent the model from being saved.
"""

from django.db import models
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.conf import settings

class Project(models.Model):
    icon = models.ImageField(upload_to='project_icons/', blank=True)
    name = models.CharField(max_length=100, unique=True)
    key = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    #lead = models.ForeignKey(User, on_delete=models.CASCADE) #not more working with django-tenant-users
    lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Participants(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #not more working with django-tenant-users
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Project Participants'
        verbose_name_plural = 'Project Participanats'

    def clean(self):
        if self.user is None and self.role is None:
            raise ValidationError('Either user or group must be set')

    def __str__(self):
        if self.user is not None:
            return f"{self.user.username} in {self.project.name}"
        elif self.role is not None:
            return f"{self.role.name} in {self.project.name}"
        else:
            return f"No user or group in {self.project.name}"


