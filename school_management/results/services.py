# results/services.py
from django.db import transaction
from django.db.models import Sum
from academics.models import ClassRoom, Subject, Student
from assessments.models import Period, Grade, Evaluation
from .models import SubjectResult, PeriodResult, AnnualResult


class ResultCalculationService:
    """Moteur de calcul pour l'application results."""

    @classmethod
    @transaction.atomic
    def calculate_period_results(cls, classroom: ClassRoom, period: Period):
        """
        1. Calcule le résultat par cours (SubjectResult) pour chaque élève.
        2. Calcule le total général de la période (PeriodResult) pour chaque élève.
        3. Calcule et attribue les rangs de la classe pour la période.
        """
        students = Student.objects.filter(classroom=classroom, is_active=True)
        subjects = Subject.objects.filter(classrooms=classroom)

        for student in students:
            period_obtained_total = 0.0
            period_max_total = 0.0

            # 1. Calcul pour chaque matière
            for subject in subjects:
                # Somme des notes obtenues par l'élève dans ce cours et cette période
                obtained = Grade.objects.filter(
                    student=student,
                    evaluation__subject=subject,
                    evaluation__period=period
                ).aggregate(total=Sum('score'))['total'] or 0.0

                # Somme des maxima des évaluations existantes créées pour ce cours/période
                max_score = Evaluation.objects.filter(
                    classroom=classroom,
                    subject=subject,
                    period=period
                ).aggregate(total=Sum('max_score'))['total'] or 20.0  # Valeur par défaut si aucune évaluation

                percentage = (obtained / max_score * 100) if max_score > 0 else 0.0

                # Enregistrement / Mises à jour dans SubjectResult
                SubjectResult.objects.update_or_create(
                    student=student,
                    subject=subject,
                    period=period,
                    defaults={
                        'obtained_score': obtained,
                        'max_score': max_score,
                        'percentage': round(percentage, 2)
                    }
                )

                period_obtained_total += obtained
                period_max_total += max_score

            # 2. Enregistrement / Mises à jour dans PeriodResult (sans le rang pour l'instant)
            period_percentage = (period_obtained_total / period_max_total * 100) if period_max_total > 0 else 0.0

            PeriodResult.objects.update_or_create(
                student=student,
                period=period,
                defaults={
                    'total_obtained': period_obtained_total,
                    'total_max': period_max_total,
                    'percentage': round(period_percentage, 2)
                }
            )

        # 3. Attribuer les rangs dans la classe pour cette période
        cls._assign_period_ranks(classroom, period)

    @classmethod
    def _assign_period_ranks(cls, classroom: ClassRoom, period: Period):
        """Trie les élèves par note obtenue décroissante et attribue leur rang."""
        period_results = PeriodResult.objects.filter(
            student__classroom=classroom,
            period=period
        ).order_by('-total_obtained')

        for rank, result in enumerate(period_results, start=1):
            result.rank = rank
            result.save(update_fields=['rank'])

    @classmethod
    @transaction.atomic
    def calculate_annual_results(cls, classroom: ClassRoom, academic_year):
        """
        Consolide toutes les périodes de l'année scolaire pour générer l'AnnualResult.
        """
        students = Student.objects.filter(classroom=classroom, is_active=True)

        for student in students:
            # Récupère tous les PeriodResult de l'élève pour l'année en cours
            period_results = PeriodResult.objects.filter(
                student=student,
                period__academic_year=academic_year
            )

            annual_obtained = period_results.aggregate(total=Sum('total_obtained'))['total'] or 0.0
            annual_max = period_results.aggregate(total=Sum('total_max'))['total'] or 0.0
            annual_percentage = (annual_obtained / annual_max * 100) if annual_max > 0 else 0.0

            AnnualResult.objects.update_or_create(
                student=student,
                academic_year=academic_year,
                defaults={
                    'total_obtained': annual_obtained,
                    'total_max': annual_max,
                    'percentage': round(annual_percentage, 2)
                }
            )

        # Attribuer les rangs annuels
        annual_results = AnnualResult.objects.filter(
            student__classroom=classroom,
            academic_year=academic_year
        ).order_by('-total_obtained')

        for rank, result in enumerate(annual_results, start=1):
            result.rank = rank
            result.save(update_fields=['rank'])