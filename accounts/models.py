from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name
    
    
class Goup(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name