from django.conf import settings
import requests


class Platform(object):


    # The Amcrest platform supports 360 degrees horiz and about 120 degrees vertical.
    # azimuth goes clockwise from 180deg behind to 360deg in front,
    #     counterclockwise from 180deg behind to 0deg in front
    # zenith goes from settings.PLATFORM_MINIMUM_ZENITH = -10deg to 0deg horizontal,
    #     to settings.PLATFORM_MAXIMUM_ZENITH (~100deg) straight up
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
