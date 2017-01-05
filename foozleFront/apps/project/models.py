from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField


class Project(models.Model):
    name = models.CharField("Name", max_length=100)
    active = models.BooleanField("Active", default=True)

    def __unicode__(self):
        return self.name


class Error(models.Model):
    project = models.ForeignKey(Project)
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField("Issue resolved", default=False)
    resolved_time = models.DateTimeField(auto_now=False)
    resolved_user = models.ForeignKey(User)
    data = JSONField(default=dict, blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.id, self.project)
