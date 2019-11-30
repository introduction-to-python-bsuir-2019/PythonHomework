import os
from urllib import request
from base64 import b64encode


class ImageDownloader:

    @staticmethod
    def get_image(url, image_dir):
        image_path = ImageDownloader.download_image(url, image_dir)
        return ImageDownloader.convert_image_to_binary(image_path)

    @staticmethod
    def download_image(url, image_dir):
        if url is not None:
            begin_name_index = url.rfind("/") + 1
            end_name_index = url.rfind('.') if url.rfind('.') > begin_name_index else -1
            image_name = url[begin_name_index:end_name_index]
            image_path = os.path.join(image_dir, image_name)
            if not os.path.exists(image_path):
                request.urlretrieve(url, image_path)
            return image_path
        else:
            return None

    @staticmethod
    def convert_image_to_binary(image_path):
        if image_path is not None:
            with open(image_path, 'rb') as f:
                return b64encode(f.read()).decode()
        else:
            return ""
