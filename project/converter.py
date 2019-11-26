from .reader import output, progress


class Converter():
    """docstring for Converter"""

    def to_json(feed, column, verbose):
        output("Convert to json...", verbose=verbose)
        counter = 0
        if verbose:
            progress(len(column), counter)
        json = '{\n  "title": "' + feed + '",\n  "news": ['
        separ = False
        for news in column:
            if separ:
                json += ','
            separ = True
            json += '{\n      "title": "' + news[0] + '",'
            json += '\n      "date": "' + news[1] + '",'
            json += '\n      "link": "' + news[2] + '",'
            json += '\n      "description": "' + news[3] + '",'
            json += '\n      "links": ['
            links = ""
            for lin in news[4]:
                links += f'\n        "{lin}",'
            if len(links) != 0:
                json += links[:-1] + "\n      ]"
            else:
                json += ']'
            json += "\n    }"
            counter += 1
            if verbose:
                progress(len(column), counter)
        json += ']\n}'
        return json
