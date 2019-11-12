import requests
import base64
import shutil


ROOT_LOGGER_NAME = 'RssReader'
MODULE_LOGGER_NAME = ROOT_LOGGER_NAME + '.to_fb2_converter'


binary = ''


def _get_image_as_base64(image_url: str) -> str:
	logger = logging.getLogger(MODULE_LOGGER_NAME + '._get_image_as_base64')
	logger.info('Getting base64-code of image')

	resp = requests.get(image_url, stream=True)

	with open('temp_img', 'wb') as img:
		resp.raw.decode_content = True
		shutil.copyfileobj(resp.raw, img)

	with open('temp_img', 'rb') as img:
		encode_str = base64.b64encode(img.read())

	return encode_str.decode('ascii')


def _add_image_binary(image_url: str, image_name: str) -> None:
	logger = logging.getLogger(MODULE_LOGGER_NAME + '._add_image_binary')
	logger.info('Add base64-code of image to binary-block')

	global binary
	binary += f'''<binary id="{image_name}" content-type="image/png">{_get_image_as_base64(image_url)}</binary>'''


def header(title: str, subtitle: str, image_url: str) -> str:
	logger = logging.getLogger(MODULE_LOGGER_NAME + '.header')
	logger.info('Return header of xml(fb2) format')

	image_name = 'cover.png'
	_add_image(image_url, image_name)
	return f'''
	<FictionBook  xmlns:l="http://www.w3.org/1999/xlink">
	<description>
	</description>
	<body>
	<title>
	<p>NEWS BY {title}</p>
	</title>
	<p>{subtitle}</p>
	<image l:href="#{image_name}"/>
	'''


def tail() -> str:
	logger = logging.getLogger(MODULE_LOGGER_NAME + '.tail')
	logger.info('Return tail of xml(fb2) format')

	return f'''
	</body>
	{binary}
	</FictionBook>'''


img_iter = -1


def section(title: str, date: str, content: str, link: str, image_url: str) -> str:
	logger = logging.getLogger(MODULE_LOGGER_NAME + '.section')
	logger.info('Return section of xml(fb2) format')
	
	global img_iter
	img_iter += 1

	try:
		_add_image_binary(image_url, f'img{img_iter}.png')
	except requests.exceptions.MissingSchema:
		pass

	return f'''
	<section>
	<title>
	<p>{title}</p>
	</title>
	<p>{date}</p>
	<p>{link}</p>
	<empty-line/>
	<image l:href="#img{img_iter}.png"/>
	<empty-line/>
	<p>{content}</p>
	<empty-line/>
	</section>
	'''
