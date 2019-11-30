import logging


class ToHtml:
    """Class responsible for converting data to html"""
    def __init__(self, news, path="./news.html"):
        self.news = news
        self.path = path
        self.html = self.make_html()

    def make_html(self):
        """Create html"""
        logging.info("Creating html")
        html = """
            <!DOCTYPE HTML>
            <html>
             <head>
              <title>News</title>
             </head>
             <body>
        """
        for entry in self.news:
            html += f"<h3><p align=\"center\">{entry.title}</p></h3>"
            html += f"<p>Channel name: {entry.channel_name}</p>"
            html += f"<p>Date: {entry.date}</p>"
            html += f"<p><a href={entry.link}>Link</a></p>"
            for img in entry.images:
                html += f"<p><img src=\'{img}\' width=\"700\" height=\"500\"></p>"
            html += f"<p>{entry.summary}</p>"
            if len(entry.links) > 0:
                counter = 0
                html += "<p>Links in the article:</p>"
                for link in entry.links:
                    counter += 1
                    html += f"<p><a href={link}>Link №{counter}</a></p>"
        html += "</body></html>"
        return html

    def make_file(self):
        """Create html file"""
        logging.info("Creating html file")
        try:
            with open(self.path, 'w') as f:
                f.write(self.html)
        except:
            print("Saving file error. Problems with path")
