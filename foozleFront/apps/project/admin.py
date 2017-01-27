from django.contrib import admin
from .models import Project, Error, InternalErrors


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'active')


class InternalErrorsAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'data')


class ErrorAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'project', 'data')

admin.site.register(Project, ProjectAdmin)
admin.site.register(InternalErrors, InternalErrorsAdmin)
admin.site.register(Error, ErrorAdmin)
