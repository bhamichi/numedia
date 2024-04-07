from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from tenant_users.tenants.models import UserProfile
from django.contrib.auth.models import AbstractUser



class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class Domain(DomainMixin):
    pass

'''
AJouter le modèle TenantUser est lié aux modèles Client et Domain qui 
se trouvent dans l'application Backend. 
'''

class TenantUser(UserProfile):
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(
        default=True,
        help_text='Designates whether the user can log into this admin site.',)
    is_superuser = models.BooleanField(
        default=True,
        help_text='Designates whether the user is a super user.',)
