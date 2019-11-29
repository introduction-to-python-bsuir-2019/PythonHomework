import pickle
import os


class Saver:
    def __init__(self, news_list):
        self.news_list = news_list
        self.date_handler = {}

    def sort(self):
        for news in self.news_list:
            if news.parsed_date in self.date_handler:
                self.date_handler[news.parsed_date].append(news)
            else:
                self.date_handler[news.parsed_date] = [news, ]

    def save(self):
        for date in self.date_handler:
            if os.path.exists("./Cache/" + date):
                with open("./Cache/" + date, 'rb') as f:
                    old_date = pickle.load(f)
                with open("./Cache/" + date, 'wb') as f:
                    pickle.dump(old_date + self.date_handler[date], f)
            else:
                with open("./Cache/" + date, 'wb') as f:
                    pickle.dump(self.date_handler[date], f)

    def start_saving(self):
        self.sort()
        self.save()
