import requests
from bs4 import BeautifulSoup
from ..date_converter import DateConverter
from ..clean_text import clean_text
from ..advertisement import Advertisement

class MuzikantenBankNet():

    def __init__(self, search_query: str, get_all_ads=False):
        '''search_query can be a normal sentence. Example: gitarist gelderland metal'''
        self.base_url = 'https://www.muzikantenbank.net'

        self.search_query = search_query
        self.replace_spaces = self.search_query.replace(' ', '+')

        self.final_url = f'{self.base_url}/advertenties/zoek?q={self.replace_spaces}'
        self.get_all_ads = get_all_ads
        if self.get_all_ads:
            self.final_url = f'{self.base_url}/advertenties/muzikanten'
        self.results = self.search_website(url=self.final_url)

    def search_website(self, url) -> list:
        '''Returns a list of dictionaries with info all advertisements'''

        self.response = requests.get(url=url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.all_advertisements = []
        self.advertisements = self.soup.find_all('article', class_='card')
        for ad in self.advertisements:
            self.title = clean_text(ad.find('span', class_='break-words').text)

            full_category = ad.find('div', class_='mt-auto')
            self.category = clean_text(ad.find('div', class_='flex-wrap').text)
            
            self.date = full_category.find('span').text
            self.date_converter = DateConverter(self.date)
            self.date_dict = self.date_converter.convert_str_to_date_muzikantenbank_net()
            self.date = self.date_converter.convert_to_datetime_object(self.date_dict)
            # TODO DATE CONVERTER
            self.message = clean_text(ad.find('p').text)
            self.link = ad.find('a', class_='mb-browse-row-card__stretch').attrs['href']
            self.link = f'https://www.muzikantenbank.net{self.link}'
            print(self.link)
            self.info = Advertisement(self.title, self.category, self.message, self.link, self.date, 'muzikantenbank.net')


            self.all_advertisements.append(self.info)

        return self.all_advertisements

