from images.models import Image
from platform.platform import Platform
from thermalcam.camera import ThermalCam

def snap_thermal():
    p = Platform()
    (azimuth, zenith) = p.get_position()
    c = ThermalCam()
    id = c.capture_image()
    i = Image(id=id, azimuth=azimuth, zenith=zenith)
    i.save()
    print id
    
