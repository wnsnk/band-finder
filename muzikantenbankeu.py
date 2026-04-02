import requests
from bs4 import BeautifulSoup
from typing import Literal

instrument_options = ['accordeonist', 'bassist', 'blazer', 'dj', 'drummer', 'geluidstechnicus',
                      'gitarist', 'percussionist', 'strijker', 'toetsenist', 'zanger-zangeres', 'overig']

province_options_netherlands = ['drenthe', 'flevoland', 'friesland', 'gelderland', 'groningen',
                                'limburg', 'noord-brabant', 'noord-holland', 'overijssel', 'utrecht', 'zeeland', 'zuid-holland']

province_options_belgium = ['antwerpen', 'henegouwen', 'limburg', 'luik', 'luxemburg',
                            'namen', 'oost-Vlaanderen', 'vlaams-brabant', 'waals-brabant', 'west-vlaanderen']


class MuzikantenBankEU():
    '''Required params: looking_for.'''

    def __init__(self, looking_for: Literal['band', 'musician'],
                 instrument: Literal[None, 'accordeonist', 'bassist', 'blazer', 'dj', 'drummer', 'geluidstechnicus',
                                     'gitarist', 'percussionist', 'strijker', 'toetsenist', 'zanger-zangeres', 'overig'] = None,
                 country: Literal['netherlands', 'belgium'] = 'netherlands', province: Literal[None, 'drenthe', 'flevoland', 'friesland', 'gelderland', 'groningen', 'limburg', 'noord-brabant', 'noord-holland', 'overijssel', 'utrecht', 'zeeland', 'zuid-holland', 'antwerpen', 'henegouwen', 'limburg', 'luik', 'luxemburg',
                                                                                               'namen', 'oost-Vlaanderen', 'vlaams-brabant', 'waals-brabant', 'west-vlaanderen'] = None,
                 city=None):
        self.base_url = 'https://www.muzikantenbank.eu'

        self.band_or_musician = self.check_band_or_musician(
            looking_for)

        self.instrument = self.check_instrument(instrument)

        self.country = self.check_country(country=country)

        self.province = self.check_province(province, country=country)

        self.city = city

        self.url_parts = [self.band_or_musician]
        if self.instrument:
            self.url_parts.append(self.instrument)
        self.url_parts.append(self.country)
        if self.province:
            self.url_parts.append(self.province)
        if self.city:
            self.url_parts.append(self.city)

        final_url = f'{self.base_url}/advertenties/' + '/'.join(self.url_parts)
        print(final_url)
        # self.search_website(url=self.final_url)

    def search_website(self, url) -> list:
        '''Returns a list of dictionaries with info all advertisements'''

        self.response = requests.get(url=url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.all_advertisements = []
        self.advertisements = self.soup.find_all('article')
        for ad in self.advertisements:
            self.title = ad.find('h1').text
            self.date = ad.find('time').text
            self.message = ad.find('p').text
            self.link = ad.find('a', href=True)['href']
            self.link = f'{self.base_url}{self.link}'
            self.info = {
                'title': self.title,
                'message': self.message,
                'link': self.link,
                'date': self.date
            }
            self.all_advertisements.append(self.info)

        return self.all_advertisements

    def check_band_or_musician(self, looking_for):
        '''checks if you are looking for a band or a musician and returns the correct string for the URL'''
        if looking_for != 'band' and looking_for != 'musician':
            raise ValueError('looking_for must be "band" or "musician"')
        elif looking_for == 'band':
            self.looking_for_band = True
        else:
            self.looking_for_band = False

        if self.looking_for_band:
            return 'muzikanten-gezocht'
        else:
            return 'muzikanten-aangeboden'

    def check_country(self, country):
        '''checks country and returns the country name in dutch for the URL'''
        if country != 'netherlands' and country != 'belgium':
            raise ValueError('country has to be "netherlands" or "belgium".')
        elif country == 'netherlands':
            return 'nederland'
        else:
            return 'belgie'

    def check_province(self, province, country):
        if province == None or province == 'None' or province == 'none':
            return None
        elif country == 'netherlands' and province in province_options_netherlands:
            return province
        elif country == 'belgium' and province in province_options_belgium:
            return province
        else:
            return ValueError('ERROR: please check province')

    def check_instrument(self, instrument):
        '''Checks if instrument is in instrument_options and returns instrument or None'''
        if instrument == None or instrument == 'None' or instrument == 'none':
            return None
        elif instrument in instrument_options:
            return instrument
        else:
            raise ValueError('ERROR: Make sure you typed in dutch. ')
