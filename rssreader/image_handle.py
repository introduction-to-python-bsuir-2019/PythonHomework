"""Module which works with iamges."""
import logging
import os

import requests
import base64
import shutil
from PIL import Image


ROOT_LOGGER_NAME = 'RssReader'
MODULE_LOGGER_NAME = ROOT_LOGGER_NAME + '.image_handle'


TEMP_IMG_NAME = 'temp_img.jpg'


def save_image_by_url(image_url: str, filepath: str):
	"""Save image to file with filepath from url with image_url."""
	logger = logging.getLogger(MODULE_LOGGER_NAME + '.save_image_by_url')
	logger.info('Saving image from image_url to filepath')

	resp = requests.get(image_url, stream=True)

	with open(filepath, 'wb') as img:
		resp.raw.decode_content = True
		shutil.copyfileobj(resp.raw, img)

	im = Image.open(filepath)
	im.save(filepath, "PNG")


def get_image_as_base64(image_url: str) -> str:
	"""Get image's encoding of base64."""
	logger = logging.getLogger(MODULE_LOGGER_NAME + '.get_image_as_base64')
	logger.info("Get image's encoding of base64")

	save_image_by_url(image_url, TEMP_IMG_NAME)

	with open(TEMP_IMG_NAME, 'rb') as img:
		encode_str = base64.b64encode(img.read())

	os.remove(TEMP_IMG_NAME)

	return encode_str.decode('ascii')