import requests
from bs4 import BeautifulSoup
from config import BASE_LINK
from abc import ABC, abstractmethod
import json
from parser_ import AdvertisementPageParser

class CrawlerBase(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data):
        pass
    @staticmethod
    def get(url):
        try:
            
            response = requests.get(url) 
           
        except Exception  as  ex: 
            return None
        return response


class LinkCrawler(CrawlerBase):
    def __init__(self, cities, link=BASE_LINK):
        self.cities = cities
        self.link = link
    
    def find_links(self,resp_text):
        soup  = BeautifulSoup(resp_text, 'html.parser')
        adv_list = soup.find_all('a')
        
        return adv_list
    
    def start_crawl_city(self,url):   
        adv_links = []   
        response = self.get(url)  
        if response is None:
            return adv_links
        new_links = self.find_links(response.text)
        adv_links.extend(new_links)
        return adv_links
    

    def start(self):
        adv_links = []
        for city in self.cities:
            links = self.start_crawl_city(self.link.format(city))
            adv_links.extend(links)
            for link in links:
                print(link.get('href'))

        self.store([li.get('href') for li in adv_links])
    
    def store(self, data):
        with open('data.json', 'a') as f:
            f.write(json.dumps(data))


class DataCrawler(CrawlerBase):
    def __init__(self):
        self.links = self.__load_links()



    @staticmethod
    def __load_links():
        with open('data.json') as f:
            links = json.loads(f.read())

        return links
    
    def start(self):
        for link in self.links:
            response = self.get(link)
            
            adv_page_parser = AdvertisementPageParser()
            data = adv_page_parser.parse(response.text)
            self.store(data)

    def store(self, data):
        with open('pages_data.json', 'a') as f:
            f.write(json.dumps(data))