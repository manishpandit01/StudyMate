from django.contrib import admin

from study_mate.models import Subject

# Register your models here.


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "semester", "created_at")
    list_filter = ("semester", "created_at")
    search_fields = ("name", "user__username")
