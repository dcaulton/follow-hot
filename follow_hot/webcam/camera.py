from io import BytesIO
import requests

from django.conf import settings

class WebCam(object):

    def __init__(self, *args, **kwargs):
        pass

    def capture_image(self, filename):
        the_url = 'http://{0}:{1}@{2}/cgi-bin/snapshot.cgi?'.format(
            getattr(settings, 'PLATFORM_USERNAME', None),
            getattr(settings, 'PLATFORM_PASSWORD', None),
            getattr(settings, 'PLATFORM_HOSTNAME', None),
        )
        response = requests.get(the_url)
        
        if response.status_code == 200:
            with open(filename, 'wb') as fd:
                fd.write(response.content)
            return
        raise Exception('bad return code from getting webcam image: {0}'.format(response.status_code))
