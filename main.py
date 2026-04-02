from muzikantenbankeu import MuzikantenBankEU
from dict_to_text import DictToText
muzikantenbank_eu = MuzikantenBankEU('musician', instrument='bassist',
                                     province='gelderland', )


with open('muzikantenbank_eu_results.txt', 'a') as muzbanktxt:
    for thing in muzikantenbank_eu.results:
        dict_to_text = DictToText(thing)
        muzbanktxt.write(f'{dict_to_text.return_advertisement()}\n')
