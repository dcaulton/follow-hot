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
    if image1.azimuth != image2.azimuth or image1.zenith != image2.zenith:
        print 'warning: diffing two images at diff coordinates is kinda silly'
    cv2_image1 = cv2.imread(image1.path)
    cv2_image2 = cv2.imread(image2.path)
    image3 = Image(id=uuid.uuid4(), azimuth=image1.azimuth, zenith=image1.zenith)
    cv2_image3 = cv2.subtract(cv2_image1, cv2_image2)
    cv2.imwrite(image3.path, cv2_image3)
    image3.save()
    return image3
