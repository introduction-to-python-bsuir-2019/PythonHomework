import pickle
import os
import logging


class Saver:
    """The class is responsible for saving and unloading data."""
    def sort(self, news_list):
        """The method sorts news from the link by date"""
        logging.info("Sorting news in saver")
        date_handler = {}
        for news in news_list:
            if news.parsed_date in date_handler:
                date_handler[news.parsed_date].append(news)
            else:
                date_handler[news.parsed_date] = [news, ]
        return date_handler

    def save(self, date_handler):
        """Save data"""
        logging.info("Saving data")
        for date in date_handler:
            if os.path.exists("./Cache/" + date):
                with open("./Cache/" + date, 'rb') as f:
                    old_date = pickle.load(f)
                delete_list = []
                for new_d in date_handler[date]:
                    for old_d in old_date:
                        if str(new_d) == str(old_d):
                            delete_list.append(new_d)
                for new_d in delete_list:
                    date_handler[date].remove(new_d)
                with open("./Cache/" + date, 'wb') as f:
                    pickle.dump(old_date + date_handler[date], f)
            else:
                with open("./Cache/" + date, 'wb') as f:
                    pickle.dump(date_handler[date], f)

    def start_saving(self, news_list):
        try:
            handler = self.sort(news_list)
            self.save(handler)
        except Exception as e:
            logging.error("Saving error")
            logging.error(str(e))

    def load(self, date):
        """Load data from files"""
        logging.info("Loading data from files")
        if not os.path.exists("./Cache/" + date):
            return None
        with open("./Cache/" + date, 'rb') as f:
            old_news = pickle.load(f)
        return old_news
