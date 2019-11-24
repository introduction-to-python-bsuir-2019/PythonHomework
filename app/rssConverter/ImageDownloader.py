import os
from urllib import request
from base64 import b64encode


def get_image(url, image_dir):
    image_path = download_image(url, image_dir)
    return convert_image_to_binary(image_path)


def download_image(url, image_dir):
    image_name = url[url.rfind("/")+1:]
    image_path = os.path.join(image_dir, image_name)
    if not os.path.exists(image_path):
        request.urlretrieve(url, image_path)
    return image_path


def convert_image_to_binary(image_path):
    with open(image_path, 'rb') as f:
        return b64encode(f.read()).decode()
