from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Permission
from companies.models import Enterprise

class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name
    
    
class Group(models.Model):
    name = models.CharField(max_length=150)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class GroupPermissions(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    
class UserGroups(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
