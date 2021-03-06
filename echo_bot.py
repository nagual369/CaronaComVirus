# coding=utf-8
import telebot  # библиотеки
from covid import Covid
from telebot import types
from countryinfo import CountryInfo

bot = telebot.TeleBot('1191501364:AAHRwcfipu_lnJp_g902GDDNJoJzwTm12BE')  # токен

covid = Covid(source="worldometers")

data = covid.get_data()  # all info


@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Belgium')
    item2 = types.KeyboardButton('World')
    item3 = types.KeyboardButton('Netherlands')
    item4 = types.KeyboardButton('Italy')
    item5 = types.KeyboardButton('Russia')
    item6 = types.KeyboardButton("Other")
    markup.row(item2)
    markup.row(item1, item5, item3)
    markup.row(item4, item6)
    bot.send_message(message.chat.id,
                     'Приветствую тебя!Этот бот покажет тебе мировую статистику случаев заражения\n'
                     ' Covid 19, а именно зафиксированное количество\n'
                     ' инфицированных, погибших и выздоровевших.\n'
                     'Посмотри на клавиатуру и выбери интересующую тебя страну\n'
                     ' или напиши в сообщении, например: "Russia".',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])  # Дейстивия бота
def pizda(message):
    # country = next((x for x in data if x['country'] == message.text))
    country = None
    for x in data:
        if x['country'] == message.text:
            country = x

    if message.text == "World":
        bot.send_message(message.chat.id, f"По миру:\n"
                                          f" Подтверждено - {country['confirmed']},\n"
                                          f" Cмертей  - {country['deaths']},\n"
                                          f" Выздоровело - {country['recovered']}\n")
    elif message.text == 'Back':
        # keyboard
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Belgium')
        item2 = types.KeyboardButton('World')
        item3 = types.KeyboardButton('Netherlands')
        item4 = types.KeyboardButton('Italy')
        item5 = types.KeyboardButton('Russia')
        item6 = types.KeyboardButton("Other")
        markup.row(item2)
        markup.row(item1, item5, item3)
        markup.row(item4, item6)
        bot.send_message(message.chat.id,
                         'Посмотри на клавиатуру и выбери свою страну или напиши в сообщении. Например "Russia"',
                         reply_markup=markup)
    elif isinstance(country, dict):
        if message.text == "USA":
            population = CountryInfo("United States").population()
        else:
            population = CountryInfo(message.text).population()
        bot.send_message(message.chat.id, f"В стране:\n"
                                          f"Численность населения - {population}\n"
                                          f" Подтверждено - {country['confirmed']},\n"
                                          f" Cмертей  - {country['deaths']},\n"
                                          f" Выздоровело - {country['recovered']}\n")
    elif message.text == "Other":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        items = [types.KeyboardButton(x['country']) for x in data]
        items.insert(0, types.KeyboardButton('Back'))
        markup.add(*items)
        bot.send_message(message.chat.id,
                         'Посмотри на клавиатуру и выбери свою страну или напиши в сообщении. Например "Russia"',
                         reply_markup=markup)

    else:
        bot.send_message(message.chat.id, "No such country")


# run
print("Running...")
bot.polling(none_stop=True)
