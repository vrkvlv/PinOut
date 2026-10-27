from django.contrib import admin

from .models import Project, ProjectComponent, Step


class ProjectComponentInline(admin.TabularInline):
    model = ProjectComponent


class StepInline(admin.TabularInline):
    model = Step


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectComponentInline, StepInline]
