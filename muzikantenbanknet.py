import requests
from bs4 import BeautifulSoup
from typing import Literal


class MuzikantenBankNet():
    '''Required params: looking_for.'''

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
            print(self.title)
            self.category = ad.find(
                style="color:rgb(34,34,34);font-size:15.5px;margin-top:2px;font-family:'Open Sans','Helvetica Neue','Helvetica',"
                "'Arial','sans-serif';").text
            print(self.category)
            self.date = None
            self.message = ad.find(class_='msg').text
            print(self.message)
            self.link = ad.find(
                'a', style='font-weigth:bold;',).text
            print(self.link)
            # self.link = f'{self.base_url}{self.link}'
            # self.info = {
            #     'title': self.title,
            #     'category': self.category,
            #     'message': self.message,
            #     'link': self.link,
            #     'date': self.date
            # }
            # self.all_advertisements.append(self.info)

        # print(self.advertisements)

        return self.all_advertisements


test = MuzikantenBankNet('bassist gelderland leuke muziek')
