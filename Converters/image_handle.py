"""Module which works with iamges."""
import logging
import os
import requests
import base64
import shutil
from PIL import Image


class ImageHandling():
    '''Class for saving and decoding images to Binary format'''

    def __init__(self):
        '''Initialize image sourse and save path'''
        logging.info('Initialize image sourse...')
        self.temp_image = 'temp_img.jpg'

    def save_image_by_url(self, image_url: str, filepath: str):
        """Save image to file with filepath from url with image_url."""
        if image_url != 'No image':
            try:
                resp = requests.get(image_url, stream=True)
            except ConnectionError:
                print('No Internet connection ')

            with open(filepath, 'wb') as img:
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, img)

            tim = Image.open(filepath)
            tim.convert('RGB').save(filepath, "PNG")

    def get_image_as_base64(self, image_url: str) -> str:
        """Make image encoding with base64 standart."""
        logging.info('Encoding with base64...')

        self.save_image_by_url(image_url, self.temp_image)

        with open(self.temp_image, 'rb') as img:
            encode_str = base64.b64encode(img.read())

        os.remove(self.temp_image)

        return encode_str.decode('ascii')
