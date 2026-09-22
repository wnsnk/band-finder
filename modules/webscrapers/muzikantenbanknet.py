import requests
from bs4 import BeautifulSoup
from date_converter import DateConverter
# REMINDER CHANGE BACK TO ..date_converter and remove date converter in webscrapers
from clean_text import clean_text


class MuzikantenBankNet():

    def __init__(self, search_query: str, get_all_ads=False):
        '''search_query can be a normal sentence. Example: gitarist gelderland metal'''
        self.base_url = 'https://www.muzikantenbank.net'

        self.search_query = search_query
        self.replace_spaces = self.search_query.replace(' ', '-')

        self.final_url = f'{self.base_url}/advertenties/text-zoeken/{self.replace_spaces}'
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

            # self.date_converter = DateConverter(self.category)
            # self.date_dict = self.date_converter.convert_str_to_date_muzikantenbank_net()
            # self.date = self.date_converter.convert_to_datetime_object(
            #     self.date_dict)
            
            self.date = full_category.find('span').text
            self.message = clean_text(ad.find('p').text)
            self.url = ad.find('a', class_='mb-browse-row-card__stretch').attrs['href']

            self.info = {
                'title': self.title,
                'category': self.category,
                'message': self.message,
                'link': self.url,
                'date': self.date,
                'website': 'muzikantenbank.net'
            }

            self.all_advertisements.append(self.info)

        return self.all_advertisements


muzbank = MuzikantenBankNet('', True)
# print(muzbank.advertisements)
