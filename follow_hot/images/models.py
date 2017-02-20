from __future__ import unicode_literals
import os

from django.db import models

class Image(models.Model):
    id = models.UUIDField(primary_key=True)
    camera_type = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now=True)
    azimuth = models.FloatField()
    zenith = models.FloatField()

    @property
    def path(self):
        return self.get_path_for_image_id(self.id)

    @classmethod
    def get_path_for_image_id(cls, id):
        return os.path.join('/tmp', str(id) + '.jpg')

    def __repr__(self):
        return 'Image {0}'.format(self.id)
