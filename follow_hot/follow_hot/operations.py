import uuid

import cv2
from PIL import Image as PIL_Image, ImageFilter

from images.models import Image
from platform.platform import Platform
from thermalcam.camera import ThermalCam
from webcam.camera import WebCam

def goto_position(azimuth, zenith):
    # positions the camera to specified a&z = (180,0) is straight ahead
    p = Platform()
    p.goto_position(azimuth, zenith)

def snap_thermal():
    # wrapper to snap a thermal pic, get position and save it as an image
    p = Platform()
    (azimuth, zenith) = p.get_position()
    c = ThermalCam()
    id = uuid.uuid4()
    image_path = Image.get_path_for_image_id(id)
    c.capture_image(image_path)
    i = Image(id=id, azimuth=azimuth, zenith=zenith, camera_type='thermal')
    i.save()
    return i

def scale_thermal_and_save(thermal_image):
    id = uuid.uuid4()
    new_image_path = Image.get_path_for_image_id(id)
    # scale image
    pil_image_in = PIL_Image.open(thermal_image.path)
    scale_method = PIL_Image.BICUBIC
    width = 640
    height = 480
    pil_image_new = pil_image_in.resize((width, height), scale_method)
    # blur scaled image
    for i in range(1, 10):
        pil_image_new = pil_image_new.filter(ImageFilter.BLUR)
    # save new image and return
    pil_image_new.save(new_image_path)
    i = Image(id=id, azimuth=thermal_image.azimuth, zenith=thermal_image.zenith, camera_type='thermal')
    i.save()
    return i

def snap_webcam():
    # wrapper to snap a webcam pic, get position and save it as an image
    p = Platform()
    (azimuth, zenith) = p.get_position()
    c = WebCam()
    id = uuid.uuid4()
    image_path = Image.get_path_for_image_id(id)
    c.capture_image(image_path)
    i = Image(id=id, azimuth=azimuth, zenith=zenith, camera_type='webcam')
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
