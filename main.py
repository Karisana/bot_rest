from datetime import datetime

import telebot
from telebot import types
import time
import random

import files_xl
from db import Database
from send import SendAdmin

bot = telebot.TeleBot('5700408483:AAGRXjw1Jac9IPXZLyMyoHilHO7wCFUjOM4')
# bot = telebot.TeleBot('997476739:AAHntotVGpgE2mISTeNrI0gVAFpsdQQoths') #ТЕСТ
# база данных
db = Database('database.db')

# отправка сообщений:
send = SendAdmin()


@bot.message_handler(content_types=['photo'])
# админ присылает фото для рассылки, функ добавляет его в словарь
def admin_send_photo(message):
    # print(message.photo.file_id)
    if message.chat.type == 'private':
        if message.from_user.id == 1020629:
            photo = max(message.photo, key=lambda x: x.height)
            send.get_img(photo.file_id)


@bot.message_handler(commands=['adminsendlink'])
# админ присылает ссылку для рассылки, функ добавляет его в словарь
def admin_send_link(message):
    if message.chat.type == 'private':
        if message.from_user.id == 1020629:
            link = message.text
            send.get_link(link)
            print(send)


@bot.message_handler(commands=['adminsendtext'])
# админ присылает текст для рассылки, функ добавляет его в словарь
def admin_send_text(message):
    if message.chat.type == 'private':
        if message.from_user.id == 1020629:
            text = message.text
            send.get_text(text)


@bot.message_handler(commands=['adminsendall'])
# фун для рассылки по бд
def send_all_mes(message):
    if message.chat.type == 'private':
        if message.from_user.id == 1020629:  # айди админа
            link = send.res_mes['link'][14:]
            text = send.res_mes['text'][14:]

            users = db.get_users()
            for row in users:
                time.sleep(1)
                try:
                    bot.send_photo(row[0], photo=send.res_mes['photo'])
                    bot.send_message(row[0], text)
                    bot.send_message(row[0], link)

                    if int(row[1]) != 1:
                        db.set_active(row[0],
                                      1)  # если пользователь не был активен, но получил наше сообщение, то меняем ему
                        # статус на активный
                    else:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[1], 0)  # не получил -  меняем на не активный статус
            bot.send_message(message.from_user.id, 'Рассылка прошла')


# меню
menu = ['Рестораны', 'Акции', 'Доставка', 'Система лояльности', 'Афиша']
key_1 = types.KeyboardButton(menu[0])
key_2 = types.KeyboardButton(menu[1])
key_3 = types.KeyboardButton(menu[2])
key_4 = types.KeyboardButton(menu[3])
key_5 = types.KeyboardButton(menu[4])

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
markup.add(key_1, key_2, key_3, key_4, key_5)

choice_menu = [['Сейчас всё сделаем', 'Не переживайте, всё будет круто!'],
               ['Илья кладет бумаги с названием рестиков в шляпу', 'Мешает - мешает - мешает...'],
               ['Опять в эти ваши игрульки играете? Ну ладно...', 'Ведётся поиск в базе данных'],
               ['Инициирую поиск ресторана твоего ресторана...', 'Где-же он...'],
               ['(Ворчит) А могли бы на работе делом заниматься', 'Ведётся поиск в базе данных'],
               ['Эй, зачем разбудили...', 'Сейчас - сейчас выберу вам ресторан, не переживайте'],
               ['Сканирую...', 'Ведётся выбор...']]

promo = ['Акции на доставку', 'Акции на самовывоз', 'Акции в ресторанах']

text_promo = 'Участие в акциях доступно при оформлении заказа через сайт milimon.ru или по телефону +7 (846) ' \
             '2000-220. Акции в бонусной системе не участвуют. Акции не суммируются друг с другом. '


def creation_menu(data, name_btm):
    menu_global = telebot.types.InlineKeyboardMarkup()

    count = 0
    for i_name in data:
        count += 1
        btm = name_btm + str(count)
        menu_global.add(telebot.types.InlineKeyboardButton(text=i_name, callback_data=btm))
    return menu_global


# стартовая команда. Она добавляет пользователя в бд, если его там нет. и отправляет главное сообщение приветствия.

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            try:
                db.add_user(message.from_user.id)
            except:
                pass
        mes = f'{message.from_user.first_name}, рады приветствовать вас в официальном чат-боте Milimon Family! ' \
              'Чтобы получить информацию о ресторанах, акциях, мероприятиях, доставке, системе лояльности ' \
              'воспользуйтесь меню бота ниже 👇🏻 '

        bot.send_message(message.chat.id, mes, parse_mode='html')
        bot.send_message(message.chat.id, text='Выберите нужный раздел:', reply_markup=markup)


@bot.message_handler(commands=['help'])
# основное меню без приветствия
def get_away(message):
    print('хелп')
    bot.send_message(message.chat.id, text='И снова вы в основном разделе. Выбирайте, что вас интересует:',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
# поиск по основному меню (пока только лояльность есть)
def step_rest(message):
    if message.text == 'Рестораны':
        markup_rest = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        rest_1 = 'Выбрать ресторан по названию'
        rest_2 = 'Удивите меня, выберите за меня!'
        away = 'Вернуться в главное меню'
        markup_rest.add(rest_1, rest_2, away)

        bot.send_message(message.from_user.id, 'Выбери нужный ответ:', parse_mode='html', reply_markup=markup_rest)

    elif message.text == 'Выбрать ресторан по названию':
        bot.send_message(message.from_user.id,
                         text='Выберите ресторан и получите необходимую информацию о нем:',
                         parse_mode='MarkdownV2', reply_markup=files_xl.restaurants.btm())

    elif message.text == 'Удивите меня, выберите за меня!':
        choice = random.choice(choice_menu)
        mes = f'<i>{choice[0]}</i>'
        bot.send_message(message.chat.id, mes, parse_mode='html')
        time.sleep(1)
        mes = f'<i>{choice[1]}</i>'
        bot.send_message(message.chat.id, mes, parse_mode='html')
        time.sleep(1)
        bot.send_message(message.chat.id, 'Выбор пал на: ')

        random_rest = random.choice(list(files_xl.restaurants.data))
        name = random_rest['name']
        menu = random_rest['menu']
        text = random_rest['info']
        adress = random_rest['adress']
        link = random_rest['link']
        number = random_rest['number']
        mes = f'<b>{name}</b>\n' \
              f'{menu}\n' \
              f'\n' \
              f'{text}\n' \
              f'\n' \
              f'<i>{adress}</i>\n' \
              f'<i>{number}</i>'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Оформить заказ', url=link, row_width=1))
        bot.send_message(message.chat.id, mes, reply_markup=markup, parse_mode='html')
    elif message.text == 'Вернуться в главное меню':
        get_away(message)

    elif message.text == 'Акции':
        mes = 'Выберите нужный раздел:'
        bot.send_message(message.from_user.id, text=mes,
                         reply_markup=creation_menu(promo, 'promo'))

    elif message.text == 'Доставка':
        mes = 'Мы уже готовы принять ваш заказ! Выберите нужный раздел:'
        bot.send_message(message.from_user.id, text=mes,
                         reply_markup=files_xl.delivery.btm())

    elif message.text == 'Система лояльности':
        mes = '<b>Путь к сердцу гостей мы прокладываем ежедневно. Не только через желудок.</b>\n' \
              'Помимо еды и напитков, ' \
              'в нашем арсенале много амурных стрел: искренний сервис, уютный интерьер, звук, свет, ' \
              'сочный видеоряд... Ещё одной стрелой, которая поможет нам покорить ваши сердца окончательно и ' \
              'бесповоротно, станет умная программа лояльности. '

        bot.send_message(message.from_user.id, text=mes, parse_mode='html',
                         reply_markup=files_xl.loyalty.btm())
    elif message.text == 'Афиша':  # доставка
        mes = 'Выберите нужный вариант:'
        bot.send_message(message.from_user.id, text=mes,
                         reply_markup=files_xl.afisha.btm())


@bot.callback_query_handler(func=lambda call: call.data.startswith('loyal'))
# поиск по системе лояльности
def step_loyal(call):
    markup = types.InlineKeyboardMarkup()
    mes = ''
    for i in files_xl.loyalty.data:
        if call.data == i['id']:
            mes = i['info']

    bot.send_message(call.from_user.id, mes, reply_markup=markup, parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith('rest'))
# поиск по ресторанам
def step_rest(call):
    markup = types.InlineKeyboardMarkup()
    for i in files_xl.restaurants.data:

        if call.data == i['id']:
            name = i['name']
            info = i['info']
            site = i['link']
            adress = i['adress']  # поменять на локацию потом
            number = i['number']
            mes = f'<b>{name}</b>\n' \
                  f'\n' \
                  f'{info}\n' \
                  f'\n' \
                  f'{adress}\n' \
                  f'\n' \
                  f'{number}'
            markup.add(types.InlineKeyboardButton('Оформить заказ', url=site, row_width=1))
            bot.send_message(call.from_user.id, mes, reply_markup=markup, parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith('12'))
def step_deli(call):
    markup = types.InlineKeyboardMarkup()
    for i in files_xl.delivery.data:
        if call.data == i['id']:
            mes = i['info']
            bot.send_message(call.from_user.id, mes, reply_markup=markup, parse_mode='html')


@bot.callback_query_handler(func=lambda call: call.data.startswith('promo'))
def step_promo(call):
    if call.data == 'promo1':
        bot.send_message(call.from_user.id, text='Выберите ресторан для просмотра акций:',
                         reply_markup=files_xl.promo_del.btm())

    elif call.data == 'promo2':
        bot.send_message(call.from_user.id, text='Выберите ресторан для просмотра акций:',
                         reply_markup=files_xl.promo_sam.btm())

    elif call.data == 'promo3':
        bot.send_message(call.from_user.id, text='Выберите ресторан для просмотра акций:',
                         reply_markup=files_xl.promo_rest.btm())


@bot.callback_query_handler(func=lambda call: call.data.startswith('del'))
def step_promo_del(call):
    link = ''
    for i in files_xl.promo_del.data:
        if call.data == i['id']:
            name_promo = i['name_promo']
            info_promo = i['info_promo']
            tel = '+7 (846) 2000-220'
            line = '_' * 30
            if len(i['link']) > 2:
                link = i['link']
            mes = f'<b>{name_promo}</b>\n' \
                  f'\n{info_promo}\n ' \
                  f'{line}\n' \
                  f'<i>{tel}</i>'
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Оформить заказ', url=link, row_width=1))
            bot.send_message(call.from_user.id, mes, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('prsa'))
def step_promo_sam(call):
    markup = types.InlineKeyboardMarkup()
    for i in files_xl.promo_sam.data:
        if call.data == i['id']:
            name_promo = i['name_promo']
            info_promo = i['info_promo']
            address = i['adress']
            tel = '+7 (846) 2000-220'
            link = i['link']
            line = '_' * 30
            markup.add(types.InlineKeyboardButton('Оформить заказ', url=link, row_width=1))
            mes = f'<b>{name_promo}</b>\n\n{info_promo}\n {line}\n' \
                  f'Забрать заказ можно по адресам:\n{address}\n\n{tel}'
            bot.send_message(call.from_user.id, mes, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('prest'))
def step_promo_sam(call):
    markup = types.InlineKeyboardMarkup()
    for i in files_xl.promo_rest.data:
        if call.data == i['id']:
            name_promo = i['name_promo']
            info_promo = i['info_promo']
            address = i['adress']
            tel = '+7 (846) 2000-220'
            line = '_' * 30
            mes = f'<b>{name_promo}</b>\n\n{info_promo}.\n{line}\nДействует по адресам:\n{address}\n\n{tel}'
            bot.send_message(call.from_user.id, mes, parse_mode='html', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('afi'))
def step_promo_sam(call):
    markup = types.InlineKeyboardMarkup()
    for i in files_xl.afisha.data:
        if call.data == i['id']:
            date = str(i['date']).lower()
            name = i['name']
            info_promo = i['info']
            address = i['adress']
            number = i['number']
            line = '_' * 30
            mes = f'<i>Месяц: {date}</i>\n<b>Ресторан {name}</b>\n{address}\n\n{info_promo}\n\n{number}'
            bot.send_message(call.from_user.id, mes, parse_mode='html', reply_markup=markup)


bot.polling(none_stop=True)
