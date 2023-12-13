from abc import ABC, abstractmethod
import requests
from product.config_crawler import storage_neme, category_name, base_url
from product.storge import FileStorage
import re


class CrawlerBase(ABC):

    @property
    def storage_set(self):
        if storage_neme == 'file':
           return FileStorage()
        # Here I want to add the condition to be added to the database

        return False

    @abstractmethod
    def start(self, store):
        pass

    @abstractmethod
    def store(self, data, filename=None):
        pass

    def get_page(self, url, start=0):
        response = requests.get(url + str(start))

        return response


class LinkCrawler(CrawlerBase):
    def __init__(self, link=base_url, category=category_name):
        self.link = link
        self.category = category
        super().__init__()

    def find_links(self, link):
        category_links = list()
        page = 1
        while True:
            url = self.link.format(link, page)
            response = self.get_page(url)

            if response.status_code == 200:
                data = response.json().get('data', [])

                if data is None or not data:
                    print(f"No more data for page {page}")
                    break

                self.store(data, 'links')
                category_links.append(data)
                print(f'Successfully crawled page {page}')
                page += 1
            else:
                print(f'Failed to crawl page {page}.'
                      f' Status code: {response.status_code}')
                break
        return category_links

    def start(self, store=True):
        list_href = list()

        for cat in self.category:
            links = self.find_links(cat)
            list_href.extend(links)
            print(f'put link to queue')
        if store:
            extracted_urls = self.extract_urls(list_href)
            self.store(extracted_urls)

        return list_href

    def extract_urls(self, data):
        pattern = r'"/product/([^"]*)"'
        matches = []

        for li in data:
            url = li.get("url", {}).get("uri", '')
            match = re.search(pattern, url)
            if match:
                matches.append({"url": match.group(1), 'flag': False})

        return matches

    def store(self, data, *args):
        self.storage_set.store(data, 'adv_links')

