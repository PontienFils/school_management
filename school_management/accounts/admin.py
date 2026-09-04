from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'matricule', 'school', 'is_active_account')
    list_filter = ('role', 'is_active_account', 'school')
    search_fields = ('user__username', 'matricule')