import requests
import telegram
from telegram.ext import Updater, JobQueue

# API kalitlari va ma’lumotlar
WEATHER_API_KEY = "62234ef5d6853366d5c5728110e25549"
TELEGRAM_TOKEN = "7525161319:AAFfCnpD4WAR7sovELkrbngQukeczLZxT9I"
CITY = "Toshkent"  # Shaharni o‘zgartirishingiz mumkin
CHAT_ID = "7342872422"  # Sizning chat ID’ingiz

# Ob-havo olish
def get_weather():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    temp = response['main']['temp']
    weather = response['weather'][0]['main']
    return temp, weather

# Botni ishga tushirish
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Ob-havo yangilash va stiker yuborish
def update_weather(context):
    temp, weather = get_weather()
    status = f"{CITY}: {temp}°C, {weather}"
    bot.set_my_description(status)  # Profil statusini yangilash

    if "Rain" in weather:
        bot.send_sticker(CHAT_ID, "CAACAgIAAxkBAAIBEGZx7p5g8sL5AAFiAAHzN9nD5gABMwAChA4AAkKvaBIiY9oZ3e81eTYE")  # Yomg‘ir stikeri
    elif "Cloud" in weather:
        bot.send_sticker(CHAT_ID, "CAACAgIAAxkBAAIBEmZx7qMAAXJy2gACaA4AAfM32cPmAAIEAAKEDgACQ69oEiJj2hnd7jYE")  # Bulut stikeri
    elif "Clear" in weather:
        bot.send_sticker(CHAT_ID, "CAACAgIAAxkBAAIBFGZx7rJ5nF9AAAGiAAHzN9nD5gABMwACaQ4AAkKvaBIiY9oZ3e81eTYE")  # Quyosh stikeri

# Botni sozlash
updater = Updater(TELEGRAM_TOKEN, use_context=True)
job_queue = updater.job_queue
job_queue.run_repeating(update_weather, interval=600, first=0)  # Har 10 daqiqada yangilash

updater.start_polling()
updater.idle()