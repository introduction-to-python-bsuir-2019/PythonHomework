import logging
import time
from App.Errors import FatalError

class News:
    """Класс служит для хранения и обработки информации свзянной с отдельной новостью."""

    def __init__(self, entry, channel_name):
        logging.info("Creating object News")
        try:
            self.parsed_date = self.pars_date(entry.published_parsed)
            self.title = entry.title
            self.date = entry.published
            self.summary = entry.summary
            self.link = entry.link
            self.channel_name = channel_name
        except Exception as e:
            raise FatalError("Problems with article processing")
        self.images = []
        self.links = []
        self.clear_text()

    def pars_date(self, struct):
        """Parsed date to string"""
        year = str(struct.tm_year)
        mon = str(struct.tm_mon)
        if len(mon) < 2:
            mon = "0" + mon
        day = str(struct.tm_mday)
        if len(day) < 2:
            day = "0" + day
        return year + mon + day


    def del_tags(self, ind1, ind2, ind3, delta=0, items=None):
        """В зависимости от входных параметров, метод может удалять ишние теги или
        сохранять ссылки на картинки"""
        logging.info("Tag processing")
        while self.summary.find(ind1) != -1:
            index1 = self.summary.index(ind1)
            index2 = self.summary[index1 + delta:].index(ind2)
            index3 = self.summary[index1:].index(ind3)
            if items is not None:
                items.append(self.summary[index1 + delta:index1 + index2 + delta])
            self.summary = self.summary[0:index1] + self.summary[index1 + index3 + 2:]

    def clear_text(self):
        """Метод запускающий del_tags() в различной конфигурации
        Это требуется, потому что на некоторых порталах в summary чатсть информации является \"мусором\""""
        logging.info("Improvement summary and and search for pictures and links")
        try:
            self.del_tags("<img src=", "\"", "/>", 10, self.images)
            self.del_tags("<a href=", "\"", "a>", 9, self.links)
            self.del_tags("<br", "<br", "/>")
            self.del_tags("</p>", "</p>", "p>")
            self.del_tags("<p>", "<p>", "p>")
            for link in self.links:
                if link == self.link:
                    self.links.remove(link)
        except Exception as e:
            logging.warning("Problems with tag parsing:\n" + str(e))

    def __str__(self):
        string = "Channel name: {0}\n" \
                 "Title: {1}\n" \
                 "Date: {2}\n" \
                 "Link: {3}\n\n" \
                 "Summary: {4}".format(self.channel_name, self.title, self.date, self.link, self.summary)
        if len(self.images) > 0:
            string = string + "\n\nImages in the article:"
            for img in self.images:
                string = string + "\n" + img
        if len(self.links) > 0:
            string = string + "\n\nLinks in the article:"
            for link in self.links:
                string = string + "\n" + link
        return string
