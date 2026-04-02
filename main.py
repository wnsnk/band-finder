from muzikantenbankeu import MuzikantenBankEU
from dict_to_text import DictToText
import datetime
muzikantenbank_eu = MuzikantenBankEU('musician', instrument='bassist',
                                     province='gelderland', )
today = datetime.datetime.now()

with open('muzikantenbank_eu_results.txt', 'a') as muzbanktxt:
    muzbanktxt.write(f'Muzikantenbank.eu results of {today}\n')
    for thing in muzikantenbank_eu.results:
        dict_to_text = DictToText(thing)
        muzbanktxt.write(f'{dict_to_text.return_advertisement()}\n')
