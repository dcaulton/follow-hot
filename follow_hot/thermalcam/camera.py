import datetime 
import os
import uuid

from django.conf import settings

class ThermalCam(object):

    def capture_image(self, filename):
        command = 'fswebcam --resolution 80x60 --no-banner {0}'.format(filename)
        if os.system(command):
            raise Exception('thermalcam command failed')
