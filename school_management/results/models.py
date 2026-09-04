# results/models.py
from django.db import models
from academics.models import AcademicYear, ClassRoom, Subject, Student
from assessments.models import Period

class SubjectResult(models.Model):
    """Résultat consolidé d'un élève pour un cours sur une période donnée"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='subject_results', verbose_name="Élève")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_results', verbose_name="Cours")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='subject_results', verbose_name="Période")
    
    # Totaux calculés
    obtained_score = models.FloatField(default=0.0, verbose_name="Total obtenu")
    max_score = models.FloatField(default=20.0, verbose_name="Maximum total (ex: /20)")
    percentage = models.FloatField(default=0.0, verbose_name="Pourcentage (%)")

    class Meta:
        unique_together = ('student', 'subject', 'period')

    def __str__(self):
        return f"{self.student} - {self.subject.name} ({self.period.name}): {self.obtained_score}/{self.max_score} ({self.percentage}%)"

class PeriodResult(models.Model):
    """Total général de l'élève pour toute la période (tous cours confondus)"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='period_results', verbose_name="Élève")
    period = models.ForeignKey(Period, on_delete=models.CASCADE, related_name='period_results', verbose_name="Période")
    
    total_obtained = models.FloatField(default=0.0, verbose_name="Total général obtenu")
    total_max = models.FloatField(default=0.0, verbose_name="Total maximum possible")
    percentage = models.FloatField(default=0.0, verbose_name="Pourcentage de la période")
    rank = models.PositiveIntegerField(null=True, blank=True, verbose_name="Place / Rrang dans la classe")

    class Meta:
        unique_together = ('student', 'period')

    def __str__(self):
        return f"{self.student} - {self.period.name} -> Total: {self.total_obtained}/{self.total_max} ({self.percentage}%) [Rang: {self.rank}]"

class AnnualResult(models.Model):
    """Bilan global annuel ou semestriel de l'élève"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='annual_results', verbose_name="Élève")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='annual_results', verbose_name="Année scolaire")
    
    total_obtained = models.FloatField(default=0.0, verbose_name="Total annuel obtenu")
    total_max = models.FloatField(default=0.0, verbose_name="Total annuel maximum")
    percentage = models.FloatField(default=0.0, verbose_name="Pourcentage annuel")
    rank = models.PositiveIntegerField(null=True, blank=True, verbose_name="Rang annuel")

    class Meta:
        unique_together = ('student', 'academic_year')

    def __str__(self):
        return f"Bilan Annuel: {self.student} ({self.academic_year.name}) - {self.percentage}%"