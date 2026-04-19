import requests
from bs4 import BeautifulSoup
from .date_converter import DateConverter


class MuzikantenBankNet():

    def __init__(self, search_query: str):
        '''search_query can be a normal sentence. Example: gitarist gelderland metal'''
        self.base_url = 'https://www.muzikantenbank.net'

        self.search_query = search_query
        self.replace_spaces = self.search_query.replace(' ', '-')

        self.final_url = f'{self.base_url}/advertenties/text-zoeken/{self.replace_spaces}'

        self.results = self.search_website(url=self.final_url)

    def search_website(self, url) -> list:
        '''Returns a list of dictionaries with info all advertisements'''

        self.response = requests.get(url=url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.all_advertisements = []
        self.advertisements = self.soup.find_all('div', class_='snippet')

        for ad in self.advertisements:
            self.title = ad.find('div', class_='snippet-title').text
            self.title = self.title.strip('\n')
            self.category = ad.find(
                style="color:rgb(34,34,34);font-size:15.5px;margin-top:2px;font-family:'Open Sans','Helvetica Neue','Helvetica',"
                "'Arial','sans-serif';").text
            self.category = self.category.strip()
            self.date_converter = DateConverter(self.category)
            self.date_dict = self.date_converter.convert_str_to_date_muzikantenbank_net()
            self.date = self.date_converter.convert_to_datetime_object(
                self.date_dict)
            self.message = ad.find(class_='msg').text
            self.message = self.message.strip()
            self.link = ad.select_one('div div h3 a')
            self.link = self.link.get('href')

            self.info = {
                'title': self.title,
                'category': self.category,
                'message': self.message,
                'link': self.link,
                'date': self.date
            }
            self.all_advertisements.append(self.info)

        return self.all_advertisements
