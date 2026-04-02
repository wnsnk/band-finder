test_dict = {'title': ***REMOVED***
***REMOVED***}


class DictToText():
    def __init__(self, dictionary):
        self.title = dictionary['title']
        self.message = dictionary['message']
        self.link = dictionary['link']
        self.date = dictionary['date']
        self.stripes = '________________________________________________________________________________________________________________________________'

    def return_advertisement(self):
        return f'{self.stripes}\n{self.title}\n{self.date}\n\n{self.message}\n\n{self.link}\n{self.stripes}\n'


test = DictToText(test_dict)
print(test.return_advertisement())
