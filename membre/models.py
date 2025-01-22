from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    date_creation = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    @classmethod
    def count_members(cls):
        return cls.objects.count()
    
class Salon(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.nom}"
    
    @classmethod
    def count_salons(cls):
        return cls.objects.count()