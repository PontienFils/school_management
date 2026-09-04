from django.contrib import admin
from .models import Period, Evaluation, Grade

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'order', 'is_closed')

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'classroom', 'period', 'max_score', 'date_evaluated')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'evaluation', 'score')