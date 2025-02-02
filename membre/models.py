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
    users = models.ManyToManyField(User, related_name="authorized_salons", blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_salons", null=True, blank=True) 
    def __str__(self):
        return f"{self.nom}"
    
    @classmethod
    def count_salons(cls):
        return cls.objects.count()

class Message(models.Model):
    salon = models.ForeignKey('Salon', on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.contenu[:20]}..."
    