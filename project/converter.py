from .log_helper import stdout_write, write_progressbar


class Converter():
    """Converter class. Convert data to some format"""

    def to_json(feed, column, verbose):
        """Take data and return it in json"""
        stdout_write("Convert to json...", verbose=verbose)
        counter = 0
        if verbose:
            write_progressbar(len(column), counter)
        json_text = '{\n  "title": "' + feed + '",\n  "news": ['
        separ = False
        for news in column:
            if separ:
                json_text += ','
            separ = True
            json_text += '{\n      "title": "' + news['title'] + '",'
            if 'date' in news:
                json_text += '\n      "date": "' + news['date'] + '",'
            json_text += '\n      "link": "' + news['link'] + '",'
            json_text += '\n      "description": "' + news['links'] + '",'
            json_text += '\n      "links": ['
            links = ""
            for lin in news['links']:
                links += f'\n        "{lin}",'
            if len(links) != 0:
                json_text += links[:-1] + "\n      ]"
            else:
                json_text += ']'
            json_text += "\n    }"
            counter += 1
            if verbose:
                write_progressbar(len(column), counter)
        json_text += ']\n}'
        return json_text
