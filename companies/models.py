from django.db import models

class Enterprise(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
  

class Employee(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    
