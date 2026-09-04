# teaching/models.py
from django.db import models
from schools.models import School
# Si tu utilises un profil utilisateur Django intégré :
# from accounts.models import UserProfile 
from academics.models import ClassRoom, Subject, AcademicYear

class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers', verbose_name="École")
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    matricule = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Matricule Professeur")
    gender = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], verbose_name="Sexe")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    biography = models.TextField(blank=True, null=True, verbose_name="Notes / Biographie")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Génération automatique du matricule professeur s'il est vide
        if not self.matricule:
            school_code = self.school.code.upper() if (self.school and self.school.code) else "SC"
            
            last_id = Teacher.objects.all().order_by('id').last()
            next_num = (last_id.id + 1) if last_id else 1
            
            # Format généré : ECOLE-PROF-0001
            self.matricule = f"{school_code}-PROF-{next_num:04d}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Prof. {self.last_name} {self.first_name} ({self.matricule})"

class TeacherAssignment(models.Model):
    """Affectation d'un professeur à un cours pour une classe et une année donnée"""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments', verbose_name="Enseignant")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_assignments', verbose_name="Cours")
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='teacher_assignments', verbose_name="Classe")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='teacher_assignments', verbose_name="Année scolaire")

    class Meta:
        unique_together = ('teacher', 'subject', 'classroom', 'academic_year')

    def __str__(self):
        return f"{self.teacher} -> {self.subject.name} en {self.classroom.name}"

class ClassTeacher(models.Model):
    """Désigne le professeur titulaire d'une classe (ex: Titulaire de la 3e A)"""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='titular_classes', verbose_name="Enseignant Titulaire")
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='titular_teacher', verbose_name="Classe")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='titular_teachers', verbose_name="Année scolaire")

    class Meta:
        unique_together = ('classroom', 'academic_year')

    def __str__(self):
        return f"Titulaire {self.teacher} pour {self.classroom.name} ({self.academic_year.name})"