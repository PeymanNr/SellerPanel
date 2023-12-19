from abc import ABC, abstractmethod
import requests
from product.config_crawler import storage_neme, category_name, base_url
from product.storge import FileStorage


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
        crawl = True
        page = 1
        while crawl:
            url = self.link.format(link, page)
            response = self.get_page(url)

            if response.status_code == 200:
                data = response.json().get('data', [])

                if data is None or not data:
                    print(f"No more data for page {page}")
                    break

                category_links.append(data)
                print(f'Successfully crawled page {page}')
                if page == 3:
                    crawl = False

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

            for item in list_href:
                products_list = item.get("products", [])

                self.store(
                    [{"url": "digikala.com" + li.get("url", {}).get("uri"),
                      'flag': False} for li in products_list])

        return list_href

    def store(self, data, *args):
        self.storage_set.store(data, 'adv_links')
