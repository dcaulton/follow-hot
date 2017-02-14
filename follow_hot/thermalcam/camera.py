import datetime 
import os

from django.conf import settings

class ThermalCam(object):

    def capture_image(self):
        now_string = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        command = 'fswebcam --no-banner {0}/{1}_thermal.jpg'.format('/tmp', now_string)
        os.system(command)
