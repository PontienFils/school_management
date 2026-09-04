# bulletins/models.py
from django.db import models
from academics.models import AcademicYear, ClassRoom, Student
from assessments.models import Period

class BulletinSnapshot(models.Model):
    """Garde une copie figée (snapshot JSON) du bulletin officiel d'un élève pour une période ou un semestre"""
    class BulletinType(models.TextChoices):
        PERIOD = 'PERIOD', 'Bulletin de Période'
        SEMESTER = 'SEMESTER', 'Bulletin de Semestre'
        ANNUAL = 'ANNUAL', 'Bulletin Annuel'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bulletin_snapshots', verbose_name="Élève")
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='bulletin_snapshots', verbose_name="Classe")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='bulletin_snapshots', verbose_name="Année scolaire")
    period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True, blank=True, related_name='bulletin_snapshots', verbose_name="Période (si applicable)")
    
    bulletin_type = models.CharField(max_length=20, choices=BulletinType.choices, default=BulletinType.PERIOD, verbose_name="Type de bulletin")
    
    # Données figées au moment de la proclamation (cours, notes, totaux, pourcentage, rang, mentions, comportement)
    data_snapshot = models.JSONField(default=dict, verbose_name="Données figées du bulletin")
    
    is_published = models.BooleanField(default=False, verbose_name="Proclamé / Validé")
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de proclamation")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_published:
            status = "Proclamé"
        else:
            status = "Brouillon"
        return f"Bulletin {self.get_bulletin_type_display()} - {self.student} ({status})"