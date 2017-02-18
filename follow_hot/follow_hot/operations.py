import uuid

import cv2

from images.models import Image
from platform.platform import Platform
from thermalcam.camera import ThermalCam

def goto_position(azimuth, zenith):
    p = Platform()
    p.goto_position(azimuth, zenith)

def snap_thermal():
    p = Platform()
    (azimuth, zenith) = p.get_position()
    c = ThermalCam()
    id = uuid.uuid4()
    image_path = Image.get_path_for_image_id(id)
    c.capture_image(image_path)
    i = Image(id=id, azimuth=azimuth, zenith=zenith)
    i.save()
    return i

def diff_images_to_file(image1, image2):
    # a little clunky but a necessary step towards doing it all in memory
    image1_path = Image.get_path_for_image_id(image1.id)
    image2_path = Image.get_path_for_image_id(image1.id)
    i1 = cv2.imread(image1_path)
    i2 = cv2.imread(image2_path)
    id = uuid.uuid4()
    image_path = Image.get_path_for_image_id(id)
    cv2.imwrite(image_path, i1-i2)
    i = Image(id=id, azimuth=999, zenith=999)
    i.save()
    return i
