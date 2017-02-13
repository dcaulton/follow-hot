from django.conf import settings
import requests


class Platform(object):


    def __init__(self, *args, **kwargs):
        pass

    def get_position(self):
        the_url = 'http://{0}:{1}@{2}/cgi-bin/ptz.cgi?action=getStatus'.format(
            getattr(settings, 'PLATFORM_USERNAME', None),
            getattr(settings, 'PLATFORM_PASSWORD', None),
            getattr(settings, 'PLATFORM_HOSTNAME', None),
        )
        response = requests.get(the_url)
        if response.status_code == 200:
            status_dict = {}
            status_dict.update([x.split('=', 1) for x in response.content.split()])
            azimuth = float(status_dict['status.Postion[0]']) # YES, Amcrest misspelled Position in their API 
            zenith = float(status_dict['status.Postion[1]'])
            return (azimuth, zenith)
        raise Exception('bad return code from getting platform position: {0}'.format(response.status_code))
