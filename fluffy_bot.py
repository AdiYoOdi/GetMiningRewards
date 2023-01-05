import telebot
import json
import pygsheets
import requests


with open("config.json") as f:
    token = json.load(f)
bot = telebot.TeleBot(token["telegramToken"])



def get_from_gs(cell_number):
    path = "googeSheets.json"
    auth = pygsheets.authorize(service_account_file=path)
    sh = auth.open('StrayLiveData')
    wks = sh[0]
    total_blocks = wks.get_value(cell_number)
    return total_blocks


@bot.message_handler(commands=['steak'])
def send_welcome(message):
    total = get_from_gs("A6")
    stray = get_from_gs("B6")
    del_number = get_from_gs("D6")
    del_blocks = get_from_gs("C6")
    total_hydra = get_from_gs("E6")
    bot.send_message(message.chat.id, f'''
📣 STRAY Pet Superstaker Block Mining Update 🐾
Total mined: {total}
STRAY: {stray}
{del_number} Delegators : {del_blocks}
Total Hydra delegated : {total_hydra}
🔨🥳
🔸Still plenty of room left for additional delegators. 🐾 💪
🔸Node is being checked regularly; everything is optimized, running smoothly, and with no down time.
🔸Big thank you to our STRAY Delegators! 🙏🏼❤️ 🐾
🔸https://tinyurl.com/StrayLive
    ''')

@bot.message_handler(commands=['quote'])
def send_welcome(message):
    quote = requests.request(url='https://api.quotable.io/random',method='get')
    bot.send_message(message.chat.id, quote.json()['content'])

@bot.message_handler(commands=['woof'])
def send_welcome(message):
    quote = requests.request(url='https://random.dog/woof.json',method='get')
    bot.send_message(message.chat.id, quote.json()['url'])

@bot.message_handler(commands=['meow'])
def send_welcome(message):
    quote = requests.get(url='https://api.thecatapi.com/v1/images/search')
    json_response = json.loads(quote.text)
    url = []
    for item in json_response:
        urls = item["url"]
        url.append(urls)
    # print(url)
    bot.send_message(message.chat.id, url)

bot.infinity_polling()














