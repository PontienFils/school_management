from django.contrib import admin
from .models import AcademicYear, ClassRoom, Student, Subject

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'is_current')

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'school')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'matricule', 'current_class', 'academic_year')
    search_fields = ('last_name', 'first_name', 'matricule')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'school', 'max_period_score')