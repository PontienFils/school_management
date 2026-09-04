# parents/models.py
from django.db import models
from schools.models import School
from accounts.models import UserProfile
from academics.models import Student

class ParentProfile(models.Model):
    """Profil spécifique pour un utilisateur ayant le rôle de Parent"""
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='parents', verbose_name="École")
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='parent_profile', verbose_name="Profil Utilisateur")
    matricule = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Matricule Parent")
    phone_number = models.CharField(max_length=30, blank=True, null=True, verbose_name="Téléphone de contact")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adresse")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Génération automatique du matricule parent s'il est vide
        if not self.matricule:
            school_code = self.school.code.upper() if (self.school and self.school.code) else "SC"
            
            last_id = ParentProfile.objects.all().order_by('id').last()
            next_num = (last_id.id + 1) if last_id else 1
            
            # Format généré : ECOLE-PAR-0001
            self.matricule = f"{school_code}-PAR-{next_num:04d}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        name = self.profile.user.get_full_name() or self.profile.user.username
        return f"Parent: {name} ({self.matricule})"

class ParentStudentLink(models.Model):
    """Table de liaison permettant de relier un parent à plusieurs élèves (ses enfants)"""
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='children_links', verbose_name="Parent")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='parent_links', verbose_name="Élève / Enfant")
    relationship_type = models.CharField(max_length=50, default="Père/Mère/Tuteur", verbose_name="Lien de parenté")

    class Meta:
        unique_together = ('parent', 'student')

    def __str__(self):
        return f"{self.parent} -> {self.student} ({self.relationship_type})"