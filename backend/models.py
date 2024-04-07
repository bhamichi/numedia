
'''
- AJouter le modèle TenantUser est lié aux modèles Client et Domain.
- TenantUser hérite de UserProfile et ajoute un champ name supplémentaire.
- Ce modèle est déjà une extension du modèle AbstractUser de Django, avec 
des champs supplémentaires pour prendre en charge les fonctionnalités 
multi-tenants. 
'''

from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from tenant_users.tenants.models import UserProfile

# Ce modèle étend 'TenantMixin', ce qui en fait un modèle de tanant.
class Client(TenantMixin):
    name = models.CharField(max_length=100)
    paid_until =  models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

# Ce modèle étend 'DomainMixin' pour représenter les domaines associés à chaque tenant.
class Domain(DomainMixin):
    pass

class TenantUser(UserProfile):
    # Ajoutez ici les champs supplémentaires dont vous avez besoin
    #name = models.CharField(max_length=100, blank = True,)
    pass
