"""Module which works with iamges."""
import requests
import base64
import shutil
from PIL import Image


TEMP_IMG_NAME = 'temp_img.jpg'


def save_image_by_url(image_url: str, filepath: str):
	"""Save image to file with filepath from url with image_url."""
	resp = requests.get(image_url, stream=True)

	with open(filepath, 'wb') as img:
		resp.raw.decode_content = True
		shutil.copyfileobj(resp.raw, img)

	im = Image.open(filepath)
	im.save(filepath, "PNG")


def get_image_as_base64(image_url: str) -> str:
	"""Get image's encoding of base64."""
	save_image_by_url(image_url, TEMP_IMG_NAME)

	with open(TEMP_IMG_NAME, 'rb') as img:
		encode_str = base64.b64encode(img.read())

	return encode_str.decode('ascii')