# results/utils.py
from assessments.models import Grade, Evaluation
from results.models import SubjectResult, PeriodResult
from academics.models import Student

def compute_student_subject_result(student, subject, period):
    """Calcule le résultat d'un élève pour un cours spécifique sur une période"""
    # 1. Récupérer toutes les évaluations de ce cours pour cette période
    evaluations = Evaluation.objects.filter(subject=subject, period=period, classroom=student.current_class)
    
    # 2. Récupérer les notes de l'élève pour ces évaluations
    grades = Grade.objects.filter(student=student, evaluation__in=evaluations)
    
    total_obtained = sum(g.score for g in grades)
    total_max = sum(e.max_score for e in evaluations)
    
    percentage = (total_obtained / total_max * 100) if total_max > 0 else 0.0
    
    # 3. Enregistrer ou mettre à jour le SubjectResult
    subject_result, created = SubjectResult.objects.update_or_create(
        student=student,
        subject=subject,
        period=period,
        defaults={
            'obtained_score': total_obtained,
            'max_score': total_max,
            'percentage': round(percentage, 2)
        }
    )
    return subject_result

def compute_class_period_results(classroom, period, subjects):
    """Calcule les totaux généraux et attribue les rangs pour toute une classe sur une période"""
    students = Student.objects.filter(current_class=classroom)
    period_results_list = []

    for student in students:
        total_obtained_student = 0.0
        total_max_student = 0.0

        # Calculer d'abord chaque cours pour cet élève
        for subject in subjects:
            res = compute_student_subject_result(student, subject, period)
            total_obtained_student += res.obtained_score
            total_max_student += res.max_score

        overall_percentage = (total_obtained_student / total_max_student * 100) if total_max_student > 0 else 0.0

        # Enregistrer ou mettre à jour le PeriodResult temporaire (sans le rang pour l'instant)
        p_result, created = PeriodResult.objects.update_or_create(
            student=student,
            period=period,
            defaults={
                'total_obtained': total_obtained_student,
                'total_max': total_max_student,
                'percentage': round(overall_percentage, 2),
                'rank': 0  # Sera mis à jour après le tri
            }
        )
        period_results_list.append(p_result)

    # Trier les résultats par pourcentage décroissant pour attribuer les rangs
    period_results_list.sort(key=lambda x: x.percentage, reverse=True)

    for index, p_res in enumerate(period_results_list, start=1):
        p_res.rank = index
        p_res.save()