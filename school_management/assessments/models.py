# assessments/models.py
from django.db import models
from academics.models import AcademicYear, ClassRoom, Subject, Student
from teaching.models import Teacher

class Period(models.Model):
    """Représente une période de notation (ex: Période 1, Période 2, Semestre 1, etc.)"""
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='periods', verbose_name="Année scolaire")
    name = models.CharField(max_length=100, verbose_name="Nom de la période (ex: Première Période)")
    order = models.PositiveIntegerField(verbose_name="Ordre (1, 2, 3...)")
    is_closed = models.BooleanField(default=False, verbose_name="Période clôturée")

    def __str__(self):
        return f"{self.name} ({self.academic_year.name})"

class Evaluation(models.Model):
    """Une évaluation concrète (ex: Interrogation de Math /10, Devoir /20)"""
    class EvaluationType(models.TextChoices):
        INTERROGATION = 'INTERROGATION', 'Interrogation'
        DEVOIR = 'DEVOIR', 'Devoir'
        TP = 'TP', 'Travail Pratique'
        EXAMEN = 'EXAMEN', 'Examen'

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='evaluations', verbose_name="Cours")
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='evaluations', verbose_name="Classe")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='evaluations', verbose_name="Enseignant")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='evaluations', verbose_name="Période")
    
    title = models.CharField(max_length=150, verbose_name="Titre / Description (ex: Interro 1 - Algèbre)")
    evaluation_type = models.CharField(max_length=30, choices=EvaluationType.choices, default=EvaluationType.INTERROGATION, verbose_name="Type")
    max_score = models.FloatField(verbose_name="Maximum (ex: 10, 20)")
    date_evaluated = models.DateField(verbose_name="Date de l'évaluation")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.subject.name} ({self.classroom.name}) [Max: {self.max_score}]"

class Grade(models.Model):
    """La note obtenue par un élève pour une évaluation donnée"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades', verbose_name="Élève")
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='grades', verbose_name="Évaluation")
    score = models.FloatField(verbose_name="Note obtenue")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'evaluation')

    def __str__(self):
        return f"{self.student} -> {self.score}/{self.evaluation.max_score} ({self.evaluation.title})"