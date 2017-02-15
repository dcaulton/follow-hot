import datetime 
import os
import uuid

from django.conf import settings

class ThermalCam(object):

    def capture_image(self):
        id = uuid.uuid4()
        filename = self.get_path_for_image(id)
        command = 'fswebcam --no-banner {0}'.format(filename)
        if not os.system(command):
            return id
        else:
            raise Exception('thermalcam command failed')

    @classmethod
    def get_path_for_image(cls, id):
        return os.path.join('/tmp', str(id) + '.jpg')

