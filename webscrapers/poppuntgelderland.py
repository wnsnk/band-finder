import requests
from bs4 import BeautifulSoup
from .date_converter import DateConverter


class PopPuntGelderlandPrikbord():

    def __init__(self):
        self.url = 'https://poppuntgelderland.nl/prikbord/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0'}
        self.results = self.search_website()

    def search_website(self) -> list:
        '''Returns a list of dictionaries with info all advertisements'''

        self.response = requests.get(url=self.url, headers=self.headers)
        self.response.raise_for_status()
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.all_advertisements = []
        self.advertisements = self.soup.find_all(class_='prikbordBlok')
        for ad in self.advertisements:
            self.title = ad.find('h3', class_='big').text
            self.category = ad.find('h4', class_='bold').text
            self.date_string = ad.find_all('h4')[1].text
            self.date_converter = DateConverter(self.date_string)
            self.date_dict = self.date_converter.convert_str_to_date_poppunt_gld()
            self.date = self.date_converter.convert_to_datetime_object(
                self.date_dict)
            self.message = ''
            self.link = ad.find('a', href=True)['href']

            self.info = {
                'title': self.title,
                'category': self.category,
                'message': self.message,
                'link': self.link,
                'date': self.date,
                'website': 'poppuntgelderland.nl'
            }
            self.all_advertisements.append(self.info)
        return self.all_advertisements
