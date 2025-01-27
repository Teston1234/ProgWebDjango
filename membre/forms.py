from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Salon

from .models import Membre

class MembreForm(ModelForm):
    class Meta:
        model = Membre
        fields = '__all__'

class createUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class connectionForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from .models import Salon
from django.contrib.auth.models import User

class SalonForm(forms.ModelForm):
    users = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez les noms d\'utilisateurs, séparés par des virgules',
        }),
        label="Utilisateurs (séparés par des virgules)"
    )

    class Meta:
        model = Salon
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_users(self):
        user_input = self.cleaned_data.get('users', '')
        usernames = [name.strip() for name in user_input.split(',') if name.strip()]
        users = User.objects.filter(username__in=usernames)

        if not users.exists():
            raise forms.ValidationError("Aucun utilisateur trouvé avec ces noms.")
        if len(users) != len(usernames):
            raise forms.ValidationError("Certains noms d'utilisateur sont invalides.")

        return users

class EditSalonForm(forms.ModelForm):
    users = forms.CharField(
        required=False,  # Permet de gérer les cas où le champ est vide
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez les noms d\'utilisateurs, séparés par des virgules',
        }),
        label="Utilisateurs (séparés par des virgules)"
    )

    class Meta:
        model = Salon
        fields = ['nom', 'description']  # Inclut les champs pertinents
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
