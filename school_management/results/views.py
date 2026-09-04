# results/views.py
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from academics.models import ClassRoom, Subject
from assessments.models import Period
from results.models import PeriodResult, SubjectResult
from results.utils import compute_class_period_results

@login_required
def class_results_dashboard(request, classroom_id, period_id):
    classroom = get_object_or_404(ClassRoom, id=classroom_id)
    period = get_object_or_404(Period, id=period_id)
    subjects = Subject.objects.filter(school=classroom.school)

    # 1. Déclencher le calcul automatique pour rafraîchir les totaux et les rangs
    compute_class_period_results(classroom, period, subjects)

    # 2. Récupérer les résultats triés par rang pour l'affichage
    period_results = PeriodResult.objects.filter(
        period=period, 
        student__current_class=classroom
    ).order_by('rank')

    context = {
        'classroom': classroom,
        'period': period,
        'subjects': subjects,
        'period_results': period_results,
    }
    return render(request, 'results/class_dashboard.html', context)