import os
import time
import random
import telebot
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
load_dotenv()

text_file = os.getenv('TEXT_FILE')
images_dir = os.getenv('IMAGE_DIR')
font_file = os.getenv('FONT_FILE')
repost_channel = os.getenv('REPOST_CHANNEL')
token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)

def get_text(text_file=text_file):
    with open(text_file,'r',encoding='utf-8') as file_:   
        return random.choice([l.strip() for l in file_.readlines()])

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Поделиться", callback_data="share"))
    return markup

def sign_photo(filepath, text):
    image = Image.open(filepath)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file, size=40, encoding="utf-8")
    width_image, height_image = image.size
    width_text, height_text = draw.textsize(text, font=font)
    draw.text(((width_image - width_text) / 2 + 1, ((height_image / 10) * 9) + 1),
        text, font=font, fill=(0, 0, 0, 0))
    draw.text(((width_image - width_text) / 2, ((height_image / 10) * 9)),
        text, font=font, fill=(255, 0, 0, 0))
    image.save(filepath)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привет! Присылай фотку, верну с подписью.")

@bot.message_handler(content_types=['photo'])
def image(message):
    bot.reply_to(message, "Одну секунду..")
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    file_downloaded = bot.download_file(file_info.file_path)
    file_name = "{}_{}.jpg".format(datetime.now().strftime("%Y-%m-%d_%H_%m"), message.from_user.id)
    file_path = "{}/{}".format(images_dir, file_name)
    with open(file_path, 'wb') as file_new:
        file_new.write(file_downloaded)
    text = get_text()
    sign_photo(file_path, text)
    with open(file_path, 'rb') as f:
        bot.send_photo(message.chat.id, f, reply_markup=gen_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "share":
        bot.answer_callback_query(call.id, "Отправляю!")
        bot.forward_message('-494005119', call.from_user.id, call.message.message_id)

@bot.message_handler()
def handle_help(message):
    bot.send_message(message.chat.id, text='''
    Это бот для создания мемов. \n
    Присылай фото и он добавит на него подпись. \n 
    ''')

bot.polling()