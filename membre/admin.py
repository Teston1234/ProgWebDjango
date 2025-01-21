from django.contrib import admin
from .models import Membre

# Register your models here.

class MembreAdmin(admin.ModelAdmin):
    list_display = ("prenom", "nom", "age", "date_creation")
    list_filter = ("age",)
    search_fields = ("prenom", "nom")
    date_hierarchy = "date_creation"
    ordering = ("date_creation",)
    fields = ("prenom", "nom", "age")
    readonly_fields = ("date_creation",)

admin.site.register(Membre, MembreAdmin)