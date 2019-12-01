import jinja2
import os


class ConvertTo:

    def __init__(self, feed, path):

        self.feed = feed
        self.env = None
        self.dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.path = path

        self.create_env()

    def create_env(self):
        """Creates environment for jinja2."""

        self.env = jinja2.Environment(loader = jinja2.FileSystemLoader(self.dir))

    def to_html(self):
        "Convert dictionary in HTML format."

        template = self.env.get_template('html/templ.html')
        filepath = os.path.join(os.getcwd(), self.path, self.feed['Name'] + '.html')
        with open(filepath, 'w+') as html_file:
            html_file.write(template.render(feed=self.feed))
