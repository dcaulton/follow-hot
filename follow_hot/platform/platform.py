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
            azimuth = self._convert_to_180_center(azimuth)
            zenith = float(status_dict['status.Postion[1]'])
            return (azimuth, zenith)
        raise Exception('bad return code from getting platform position: {0}'.format(response.status_code))

    def _convert_to_180_center(self, azimuth):
        # converts azimuth from the coordinate system returned by get_position, to the kind that's used by goto_position
        # incoming: degrees counterclockwise from front=360/0
        # desired: degrees clockwise from back=0
        if 0 <= azimuth <= 180:
            #its counterclockwise of straight ahead
            azimuth = 180 - azimuth
        else:
            #its to the left of straight ahead
            azimuth = 180 + (360 - azimuth)
        return azimuth

    def goto_position(self, azimuth, zenith):
        the_url = 'http://{0}:{1}@{2}/cgi-bin/ptz.cgi?action=start&channel=0&code=PositionABS'\
            '&arg1={3}&%arg2={4}&arg3=0'.format(
            getattr(settings, 'PLATFORM_USERNAME', None),
            getattr(settings, 'PLATFORM_PASSWORD', None),
            getattr(settings, 'PLATFORM_HOSTNAME', None),
            azimuth,
            zenith)
        response = requests.get(the_url)
        if response.status_code != 200:
            raise Exception('bad return code from goto platform position: {0}'.format(response.status_code))
