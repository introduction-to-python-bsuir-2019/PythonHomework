"""
    Contains class HTMLConverter which receives path
    where it will save news in HTML format
"""


import os

from app.RSSReader import RSSReader


class HTMLConverter:
    """ Writes news in HTML file """

    def __init__(self, url, limit, date, to_html, logger):
        self.url = url
        self.limit = limit
        self.date = date
        self.to_html = to_html
        self.logger = logger
        self.rss_reader = RSSReader(self.url, self.limit, self.date, self.logger)

    def create_html_code(self):
        """ Creates HTML code which contains news information """

        news = self.rss_reader.get_feed()

        html_head = self.get_html_head()
        html_foot = self.get_html_foot()
        html_entries = self.get_html_entries(news)

        html_code = html_head + html_entries + html_foot
        self.logger.info('HTML code has been created')
        return html_code

    def create_html_code_from_cache(self):
        """ Creates HTML code which contains cached news information """
        cached_feed = self.rss_reader.get_cached_json_news()

        html_head = self.get_html_head()
        html_foot = self.get_html_foot()
        html_entries = self.get_html_entries_from_cache(cached_feed)

        html_code = html_head + html_entries + html_foot
        return html_code

    def get_html_head(self):
        """ Returns HTML header code """

        html_head = '''
            <html>
                <body>
                    <p>
        '''
        return html_head

    def get_html_entries(self, news):
        """ Returns HTML code with news info """

        html_entry = ''
        html_entries = ''
        for new in news:
            entry = self.rss_reader.to_dict(new)
            html_entry = f'''
                        <strong>Title:</strong> {entry['Title']} <br />
                        <strong>Published:</strong> {entry['Published']} <br />
                        <strong>Summary:</strong> {entry['Summary']} <br />
                        <strong>Link:</strong> <a href = "">{entry['Link']}</a> <br />
                        <strong>Url:</strong> <a href = "">{entry['Url']}</a> <br />
                        <img src = "{entry['Image']}"> <br /><br />
            '''
            html_entries += html_entry
        return html_entries

    def get_html_entries_from_cache(self, entries):
        """ Returns HTML code with cached news info """

        html_entry = ''
        html_entries = ''
        for entry in entries:
            html_entry = f'''
                        <strong>Title:</strong> {entry['Title']} <br />
                        <strong>Published:</strong> {entry['Published']} <br />
                        <strong>Summary:</strong> {entry['Summary']} <br />
                        <strong>Link:</strong> <a href = "">{entry['Link']}</a> <br />
                        <strong>Url:</strong> <a href = "">{entry['Url']}</a> <br />
                        <img src = "{entry['Image']}"> <br /><br />
                    '''
            html_entries += html_entry
        return html_entries

    def get_html_foot(self):
        """ Returns HTML footer code """

        html_foot = '''
                    </p>
                </body>
            </html>
        '''
        return html_foot

    def write_to_html(self):
        """ Writes HTML code to news.html file """

        if self.date:
            file_name = 'cached_news.html'
            html_code = self.create_html_code_from_cache()
        else:
            file_name = 'news.html'
            html_code = self.create_html_code()

        try:
            file_path = self.to_html + os.path.sep + file_name
            with open(file_path, 'w', encoding='utf-8') as wf:
                wf.write(html_code)
        except FileNotFoundError:
            self.logger.info(f'Path to file {file_path} not found')
        else:
            self.logger.info('News has been written to HTML file')
