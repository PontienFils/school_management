# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from schools.models import School

class UserProfile(models.Model):
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Superadmin'
        DIRECTION = 'DIRECTION', 'Direction'
        ENSEIGNANT = 'ENSEIGNANT', 'Enseignant'
        TITULAIRE = 'TITULAIRE', 'Titulaire'
        PARENT = 'PARENT', 'Parent'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Utilisateur Django")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ENSEIGNANT, verbose_name="Rôle")
    matricule = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Matricule")
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='users', verbose_name="École rattachée")
    is_active_account = models.BooleanField(default=True, verbose_name="Compte actif")
   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        school_name = self.school.name if self.school else "Global"
        return f"{self.user.username} - {self.get_role_display()} ({school_name})"