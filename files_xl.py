import pandas
import telebot


class Files:
    def __init__(self, any_data):
        self.data = any_data
        self.data = any_data.to_dict('records')

    def info_loy(self):
        for i_data in self.data:
            yield i_data['name'], i_data['info']

    def print_loy(self, what):
        for i_data in self.data:
            if what == i_data['name']:
                return i_data['info']

    def menu_rest(self):
        for i_data in self.data:
            yield i_data['name']

    def print(self, what):
        for i_data in self.data:
            if what == i_data['name']:
                yield i_data['info'], i_data['site']

    def btm(self):
        menu_global = telebot.types.InlineKeyboardMarkup()
        test_name = ''
        for i_name in self.data:
            if test_name != i_name['name']:
                menu_global.add(telebot.types.InlineKeyboardButton(text= i_name['name'], callback_data=i_name['id']))
            test_name = i_name['name']
        return menu_global



restaurants = Files(pandas.read_excel('milimon.xlsx', sheet_name='restaurants'))
loyalty = Files(pandas.read_excel('milimon.xlsx', sheet_name='loy'))
delivery = Files(pandas.read_excel('milimon.xlsx', sheet_name='delivery'))
promo_rest =  Files(pandas.read_excel('milimon.xlsx', sheet_name='promo_rest'))
promo_sam = Files(pandas.read_excel('milimon.xlsx', sheet_name='promo_sam'))
promo_del = Files(pandas.read_excel('milimon.xlsx', sheet_name='promo_del'))
afisha = Files(pandas.read_excel('milimon.xlsx', sheet_name='afisha'))

