# 5344171006:AAGXMEsgmIbKQxO-8j01oaJBVZNEeJnuduc
import telebot
import requests
from bs4 import BeautifulSoup as Bs
from telebot import types

token = '5344171006:AAGXMEsgmIbKQxO-8j01oaJBVZNEeJnuduc'
bot = telebot.TeleBot(token=token)

# Func for starting bot


@bot.message_handler(commands=['start'])
def main_func(message):
    user = bot.send_message(
        message.chat.id, text='Hello!', reply_markup=keyboard())
    bot.register_next_step_handler(user, func_for_option)

# Func for picking choice to answer bot


def func_for_option(message):
    if message.text == 'Weather':
        func_for_city(message)
    elif message.text == 'Rates':
        func_for_rates(message)
    elif message.text == 'Lottery':
        func_for_lottery(message)
    elif message.text == 'Football Scores':
        func_for_football_scores(message)

# Func for typing city in "Weather" button


def func_for_city(message):
    buttons = types.ReplyKeyboardRemove(selective=False)
    city = bot.send_message(
        message.chat.id, text='Введіть назву міста: ', reply_markup=buttons)
    bot.register_next_step_handler(city, func_for_weather)

# Func for adding info about "Weather" from URL in bot


def func_for_weather(message):
    id = message.chat.id
    url = f'https://ua.sinoptik.ua/погода-{message.text}'
    response = requests.get(url)
    html = Bs(response.content, 'html.parser')

    # img from left side of the website near thermometer
    lst_img = [i.get("src") for i in html.find_all('img')]
    response_img = requests.get(f'https:{lst_img[8]}')
    with open('img.jpg', 'wb') as file:
        file.write(response_img.content)

    # 2nd paragraph of text
    description1 = html.select(
        '.wDescription.clearfix > .rSide > .description')[0].text
    description2 = html.select(
        '.oDescription.clearfix > .rSide > .description')[0].text

    # 1st paragraph of text
    for i in html.select('#bd2'):
        temp_min = i.select('.temperature > .min > span')[0].text
        temp_max = i.select('.temperature > .max > span')[0].text
        bot.send_sticker(id, open('img.jpg', 'rb'))
    bot.send_message(
        id, text=f'min: {temp_min} \n max: {temp_max} \n {description1} \n {description2}')

# Func for adding info about "Rates" from URL in bot


def func_for_rates(message):
    pass

# Func for adding info about "Lottery" from URL in bot


def func_for_lottery(message):
    pass

# Func for adding info about "Football Scores" from URL in bot


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

# Func for adding buttons into bot


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
