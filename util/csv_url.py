import csv
import requests
from io import StringIO

class CsvGetter:

    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url, allow_redirects=True)
        self.data = self._parse_csv()

    def _parse_csv(self):
        """
        Get the necessary information from the csv file.
        :return:
        """
        msgs = {}
        f = StringIO(self.r.text)
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            key = row[0]
            msg = row[1]
            msgs[key] = msg
        return msgs
