"""HTML converter module"""

import logging


class HTMLConverter:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name

    def dump(self):
        """Create and fill HTML-file"""
        logging.info("Create and fill HTML-file")

        html_code = f'<html>\n<head>\n<title>{self.file_name}</title>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n</head>\n<body>\n'

        for element in self.data:
            html_code += f'<b><p align="center", style="font-family:\'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; color:green; font-size: 26px">{element["title"]}</p></b>\n'
            html_code += f'<p align="center", style="font-family:\'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; color:rgb(25, 92, 25); font-size: 14px">{element["date"]}</p>\n'
            html_code += f'<p align="center", style="font-family:\'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; color:rgb(25, 92, 25); font-size: 14px"><a href="{element["link"]}">{element["link"]}</a></p>\n'
            html_code += f'<p style="font-family:\'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; color:rgb(24, 24, 24); font-size: 18px">{element["text"]}</p>\n'

            for href in element["hrefs"]:
                html_code += f'<p style="text-align:center"><img src="{href}" height="200"></p>\n'
        
        html_code += '</body>\n</html>'
        
        with open(f'{self.file_name}.html', 'w+', encoding='utf-8') as html_file:
            html_file.write(html_code)
