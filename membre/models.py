from django.db import models

# Create your models here.

class Membre(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    date_creation = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    @classmethod
    def count_members(cls):
        return cls.objects.count()