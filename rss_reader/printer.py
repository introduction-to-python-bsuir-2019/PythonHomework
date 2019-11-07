import pprint


class Printer:
    ''' Class for all output operations '''
    def stdout_print(self, feed, limit):
        ''' Print feed to cmd'''
        print(f'\nFeed: {feed["feed_name"]}\n')
        for article in feed['articles'][:limit]:
            links = ''
            num = 1
            for link in article.media['links']:
                links += '[{}]: {} (link)\n'.format(num, link)
                num += 1
            for image in article.media['images']:
                links += '[{}]: {} (image)\n'.format(num, image['source_url'])
            print('Title: {}\nDate: {}\nLink: {}\n\n{}\n\n\nLinks:\n{}'.format(article.title,
                                                                               article.date,
                                                                               article.link,
                                                                               article.content,
                                                                               links))
            print('\n'*3)

    def json_print(self, json_feed):
        '''Print feed in JSON format to cmd'''
        print(json_feed)
