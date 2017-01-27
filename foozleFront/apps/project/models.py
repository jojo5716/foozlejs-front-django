from __future__ import unicode_literals

import uuid
import httpagentparser
from django.db import models
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField


class Project(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField("Name", max_length=100)
    active = models.BooleanField("Active", default=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.token)

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

    def os(self):
        os = httpagentparser.detect(self.data['environment']['userAgent'])
        return os['os']['name']

    def browser(self):
        os = httpagentparser.detect(self.data['environment']['userAgent'])
        return os['browser']['name']


class InternalErrors(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    data = JSONField(default=dict, blank=True, null=True)

