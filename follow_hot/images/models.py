from __future__ import unicode_literals

from django.db import models

class Image(models.Model):
    id = models.UUIDField(primary_key=True)
    created_on = models.DateTimeField(auto_now=True)
    azimuth = models.FloatField()
    zenith = models.FloatField()

