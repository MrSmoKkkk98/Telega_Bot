# 5344171006:AAGXMEsgmIbKQxO-8j01oaJBVZNEeJnuduc
import telebot
import requests
from bs4 import BeautifulSoup as Bs
from telebot import types

token = '5344171006:AAGXMEsgmIbKQxO-8j01oaJBVZNEeJnuduc'
bot = telebot.TeleBot(token=token)


@bot.message_handler(commands=['start'])
def main_func(message):
    user = bot.send_message(
        message.chat.id, text='Hello!', reply_markup=keyboard())
    bot.register_next_step_handler(user, func_for_option)


def func_for_option(message):
    if message.text == 'Weather':
        func_for_weather(message)
    elif message.text == 'Rates':
        func_for_rates(message)
    elif message.text == 'Lottery':
        func_for_lottery(message)
    elif message.text == 'Football Scores':
        func_for_football_scores(message)


def func_for_weather(message):
    url = 'https://ua.sinoptik.ua/погода-київ'
    response = requests.get(url)
    html = Bs(response.content, 'html.parser')

    for i in html.select('#bd2'):
        temp_min = i.select('.temperature > .min > span')[0].text
        temp_max = i.select('.temperature > .max > span')[0].text
        bot.send_message(message.chat.id,
                         text=f'min: {temp_min}\nmax: {temp_max}')

    description1 = html.select(
        '.wDescription.clearfix > .rSide > .description')[0].text
    description2 = html.select(
        '.oDescription.clearfix > .rSide > .description')[0].text
    bot.send_message(
        message.chat.id, text=f'{description1}\n{description2}')


def func_for_rates(message):
    pass


def func_for_lottery(message):
    pass


def func_for_football_scores(message):
    url = 'https://football.ua/default.aspx?menu_id=scoreboard&dt=2022-07-02'
    response = requests.get(url)
    html = Bs(response.content, 'html.parser')

    for i in html.select('.match-center-table'):
        match_time = i.select('.match-center-table > tr > .time > a')[0].text
        first_team = i.select(
            '.match-center-table > tr > .left-team > a')[0].text
        second_team = i.select(
            '.match-center-table > tr > .right-team > a')[0].text
        score = i.select('.match-center-table > tr > .score.ended > a')[0].text
        bot.send_message(
            message.chat.id, text=f'Time: {match_time}\n{first_team} {score} {second_team}')


def keyboard():
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton(text='Weather')
    button2 = types.KeyboardButton(text='Rates')
    button3 = types.KeyboardButton(text='Lottery')
    button4 = types.KeyboardButton(text='Football Scores')
    buttons.add(button1, button2, button3, button4)
    return buttons


if __name__ == '__main__':
    bot.polling(non_stop=True)
