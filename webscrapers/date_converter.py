import datetime

muzikantenbankeu_date = 'zaterdag 14 februari 2026'
muzikantenbank_net_date = '***REMOVED***'


class DateConverter():
    def __init__(self, date):
        self.date = date
        self.dutch_months = {'januari': 1,
                             'februari': 2,
                             'maart': 3,
                             'april': 4,
                             'mei': 5,
                             'juni': 6,
                             'juli': 7,
                             'augustus': 8,
                             'september': 9,
                             'oktober': 10,
                             'november': 11,
                             'december': 12
                             }

    def convert_str_to_date_muzbank_eu(self):
        '''converts the date of muzikantenbank.eu ads to a dictionary'''
        date_splitted = self.date.split()
        self.day = date_splitted[1]
        self.month_name = date_splitted[2].lower()
        self.month = self.dutch_months[self.month_name]
        self.year = date_splitted[3]
        return {'day': self.day,
                'month': self.month,
                'year': self.year}

    def convert_str_to_date_muzikantenbank_net(self):
        '''Get's the date from the category part of muzikantenbank.net ads and turns it into a dictionary'''
        date_splitted = self.date.split()
        self.date_string = date_splitted[-4].replace(',', '')
        self.date_list = self.date_string.split('-')
        self.day = self.date_list[0]
        self.month = self.date_list[1]
        self.year = self.date_list[2]
        return {'day': self.day,
                'month': self.month,
                'year': self.year}

    def convert_to_datetime_object(self, date_dictionary):
        '''Converts a dictionary of a date into a datetime object'''
        self.date_dict = date_dictionary
        self.date_datetime = datetime.date(
            day=int(self.date_dict['day']), month=int(self.date_dict['month']), year=int(self.date_dict['year']))
        return self.date_datetime


# muzikantenbankeu = DateConverter(muzikantenbankeu_date)
# aaaaaaaa = muzikantenbankeu.convert_str_to_date_muzbank_eu()
# print(muzikantenbankeu.convert_to_datetime_object(aaaaaaaa))

# muzikantenbanknet = DateConverter(date=muzikantenbank_net_date)
# aaa = muzikantenbanknet.convert_str_to_date_muzikantenbank_net()
# print(muzikantenbanknet.convert_to_datetime_object(aaa))
