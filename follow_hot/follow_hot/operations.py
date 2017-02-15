import uuid

from images.models import Image
from platform.platform import Platform
from thermalcam.camera import ThermalCam

def snap_thermal():
    p = Platform()
    (azimuth, zenith) = p.get_position()
    c = ThermalCam()
    id = uuid.uuid4()
    image_path = Image.get_path_for_image_id(id)
    c.capture_image(image_path)
    i = Image(id=id, azimuth=azimuth, zenith=zenith)
    i.save()
