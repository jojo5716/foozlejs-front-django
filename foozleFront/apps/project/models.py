from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField


class Project(models.Model):
    token = models.CharField(max_length=36, unique=True, editable=False)
    name = models.CharField("Name", max_length=100)
    active = models.BooleanField("Active", default=True)

    def __unicode__(self):
        return self.name

    def errors_resolved(self):
        return self.error_set.filter(resolved=True).count()

    def errors_unresolved(self):
        return self.error_set.filter(resolved=False).count()


class Error(models.Model):
    project = models.ForeignKey(Project)
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField("Issue resolved", default=False)
    resolved_time = models.DateTimeField(auto_now=False, null=True)
    resolved_user = models.ForeignKey(User, null=True)
    data = JSONField(default=dict, blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.id, self.project)

    def timestamp_to_hour(self):
        return self.timestamp.strftime("%H:%M")

    def pm_or_am(self):
        return self.timestamp.strftime("%p")
