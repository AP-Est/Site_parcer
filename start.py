import requests
import threading
from extractor import LinkExtractor
from utils import time_track

sites = [
    'https://novychas.online',
    'https://www.freelancejob.ru/',
    'https://iklife.ru/udalennaya-rabota-i-frilans/poisk-raboty/vse-samye-luchshie-sajty-i-birzhi-v-internete.html',
]


class PageSizer(threading.Thread):

    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.total_bytes = 0

    def run(self):
        self.total_bytes = 0
        html_data = self._get_html(url=self.url)
        if html_data is None:
            return
        self.total_bytes += len(html_data)
        print(len(html_data))
        extractor = LinkExtractor(base_url=self.url)
        extractor.feed(html_data)
        print(extractor.links)

        for link in extractor.links:
            extra_data = self._get_html(url=link)
            if extra_data:
                self.total_bytes += len(extra_data)

    def _get_html(self, url):
        try:
            print(f'Go  {url}...')
            res = requests.get(url)
        except Exception as exc:
            print(exc)
        else:
            return res.text

@time_track
def main():
    sizers = [PageSizer(url=url) for url in sites]

    for sizer in sizers:
        sizer.start()

    for sizer in sizers:
        sizer.join()

    for sizer in sizers:
        print(f'For url {sizer.url} need download {sizer.total_bytes // 1024} Kb  = {sizer.total_bytes / 1024 / 1024} Mb')


if __name__ ==  '__main__':
    main()