from muzikantenbankeu import MuzikantenBankEU
from muzikantenbanknet import MuzikantenBankNet
from poppuntgelderland import PopPuntGelderlandPrikbord
from dict_to_text import DictToText
import datetime
muzikantenbank_eu = MuzikantenBankEU('musician', instrument='bassist',
                                     province='gelderland', )
muzikantenbank_net = MuzikantenBankNet('bassist gelderland')
poppunt_gelderland = PopPuntGelderlandPrikbord()
today = datetime.datetime.now()

with open('muzikantenbank_eu_results.txt', 'a') as muzbanktxt:
    muzbanktxt.write(f'Muzikantenbank.eu results of {today}\n')
    for result in muzikantenbank_eu.results:
        dict_to_text = DictToText(result)
        muzbanktxt.write(f'{dict_to_text.return_advertisement()}\n')

with open('muzikantenbank_net_results.txt', 'a') as muzbanktxt:
    muzbanktxt.write(f'Muzikantenbank.net results of {today}\n')
    for result in muzikantenbank_net.results:
        dict_to_text = DictToText(result)
        muzbanktxt.write(f'{dict_to_text.return_advertisement()}\n')

with open('poppuntgelderland_resulst.txt', 'a') as poppunttxt:
    poppunttxt.write(f'Poppuntgelderland results of {today}\n')
    for result in poppunt_gelderland.results:
        dict_to_text = DictToText(result)
        poppunttxt.write(f'{dict_to_text.return_advertisement()}\n')
