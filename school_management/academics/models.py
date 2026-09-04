# academics/models.py
from django.db import models
from schools.models import School

class AcademicYear(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='academic_years', verbose_name="École")
    name = models.CharField(max_length=50, verbose_name="Année scolaire (ex: 2025-2026)")
    is_current = models.BooleanField(default=False, verbose_name="Année en cours")

    def __str__(self):
        return f"{self.name} - {self.school.name}"

class ClassRoom(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes', verbose_name="École")
    name = models.CharField(max_length=100, verbose_name="Nom de la classe (ex: 3e A)")
    level = models.CharField(max_length=50, verbose_name="Niveau (ex: 3ème Humanité)")

    def __str__(self):
        return f"{self.name} ({self.school.name})"

class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    matricule = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Matricule de l'élève")
    gender = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], verbose_name="Sexe")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date de naissance")
    
    # Inscription de l'élève dans une classe pour une année scolaire donnée
    current_class = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, related_name='students', verbose_name="Classe actuelle")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='students', verbose_name="Année scolaire")

    def save(self, *args, **kwargs):
        # Génération automatique du matricule s'il est vide
        if not self.matricule:
            # On récupère l'école via la classe sélectionnée
            school_obj = self.current_class.school if self.current_class else None
            school_code = school_obj.code.upper() if (school_obj and school_obj.code) else "SC"
            year_str = str(self.academic_year.name).split('/')[-1] if self.academic_year else "2026"
            
            last_id = Student.objects.all().order_by('id').last()
            next_num = (last_id.id + 1) if last_id else 1
            
            self.matricule = f"{school_code}-{year_str}-{next_num:04d}"
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.matricule})"

class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='subjects', verbose_name="École")
    name = models.CharField(max_length=100, verbose_name="Nom du cours (ex: Mathématiques)")
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Code du cours")
    max_period_score = models.FloatField(default=20.0, verbose_name="Maximum de période par défaut")

    def __str__(self):
        return f"{self.name} (Max: {self.max_period_score})"