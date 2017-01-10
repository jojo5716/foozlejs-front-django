from django.contrib import admin
from .models import Project, Error


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'active')


admin.site.register(Project, ProjectAdmin)
