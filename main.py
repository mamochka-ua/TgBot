import telebot  # імпорт бібліотки для роботи з телеграм ботами
from config import weather_token  # імпорт токена звіта про погоду
from config import bot_token  # імпорт токена телеграм бота
import requests  # імпорт бібліотеки запросів
import datetime  # імпорт бібліотеки для роботи з часом

import http.server
import socketserver
import threading
PORT = 443  # Замініть на потрібний вам порт
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Обробка GET-запитів
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, World!')  # Відправка відповіді

# ініціалізація функції
def weather_report(city_name, weather_token):
    # ініціалізація словника з порадами
    weather_description = {
        'Thunderstorm': 'Hide under the bed today🛏',
        'Ash': 'Maybe it is time to move?✈',
        'Squall': 'Wear lead shoes to stay on feet🎈',
        'Drizzle': "It is so good at home under the covers with a cup of cocoa☕",
        'Rain': "Time for romantic walks☔",
        'Snow': 'Let it snow, let it snow, let it snow☃',
        'Mist': "Can you see your nose? I'm not👀",
        'Fog': "Can you see your nose? I'm not👀",
        'Haze': 'This is what smoking leads to🚬',
        'Smoke': 'This is what smoking leads to🚬',
        'Dust': 'Apchi💦',
        'Sand': "When everything is over, let's make a sandcastle🏰",
        'Tornado': 'Hopefully, you have a very cozy basement🚪',
        'Clear': "Don't forget your sunglasses🕶",
        'Clouds': "I am a cloud, a cloud, a cloud. I'm not a bear at all🐻"
    }

    # ініціалізація словника зі смайликами
    weather_smile = {
        'Thunderstorm': '⚡',
        'Ash': '🌋',
        'Squall': '🌬',
        'Drizzle': "🌧",
        'Rain': "🌧",
        'Snow': '🌧',
        'Mist': "🌁",
        'Fog': "🌁",
        'Haze': '🌫',
        'Smoke': '🌫',
        'Dust': '🌫',
        'Sand': "🏝",
        'Tornado': '🌪',
        'Clear': "☀",
        'Clouds': "⛅"
    }

    # виконати наступні дії
    try:
        # запрос даних з ресурсу openweather передаючи два аргументи: назва міста та погодний токен
        weather_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_token}&units=metric")
        # зберігання результатів запросу в змінній
        data = weather_request.json()

        city_name = data['name']  # надання змінній значення назви міста
        temp = data['main']['temp']  # надання змінній значення температури з обраного міста
        weather_condition = data['weather'][0]['main']  # надання змінній значення погодної умови з обраного міста
        humidity = data['main']['humidity']  # надання змінній значення вологості з обраного міста
        pressure = data['main']['pressure']  # надання змінній значення тиску з обраного міста
        wind_speed = data['wind']['speed']  # надання змінній значення швидкості вітру з обраного міста
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])  # надання змінній значення світанку з обраного міста
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])  # надання змінній значення заходу сонця з обраного міста

        if weather_condition in weather_description:    # якщо погодна умова є в словнику порад
            advice = weather_description[weather_condition]  # надання змінній значення з словника
        else:  # в інших випадках
            advice = 'Have a nice day'  # надання змінній значення поради

        if weather_condition in weather_smile:    # якщо погодна умова є в словнику смайлів
            smile = weather_smile[weather_condition]  # надання змінній значення з словника
        else:  # в інших випадках
            smile = '✨'   # надання змінній значення смайлика

        # повернення результату функції
        return f"🏙<b>Weather report for {city_name}</b>🏙\n📆Date: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n🌡Temperature: {temp}°C {weather_condition}{smile}\n💦Humidity: {humidity}%\n〽Pressure: {pressure} mmHg\n💨Wind speed: {wind_speed} m/s\n🌅Sunrise time: {sunrise}\n🌇Sunset time: {sunset}\n{advice}"

    # якщо сталася помилка
    except:
        return "This city does not exist☠"   #повернення повідомлення про помилку

# передання токена телеграм бота в функцію
bot = telebot.TeleBot(bot_token)

# ініціалізація команди старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Weather report for which city would you like to know?')  # вивід повідомлення в чат

# ініціалізація команди допомоги
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Input the name of the city and I will show you weather report')  # вивід повідомлення в чат

# ініціалізація функції для обробки текстових повідомлень
@bot.message_handler(content_types=['text'])
def get(message):
    city_name = str(message.text)  # надання змінній значення введеного з повідомлення
    bot.send_message(message.chat.id, weather_report(city_name, weather_token), parse_mode='html')  # виклик функції weather_report і вивід результату в форматі html

# ініціалізація функції для обробки всіх інших типів повідомлень
@bot.message_handler(
    content_types=['audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 'video_note', 'voice',
                   'contact', 'location', 'venue', 'dice', 'invoice', 'successful_payment', 'connected_website', 'poll',
                   'passport_data', 'web_app_data'])
def answer(message):
    bot.send_message(message.chat.id, 'Actually, it is not the name of the city🤓')  # вивід повідомлення про помилку

def run_server():
    # Створення серверу, який буде слухати вказаний порт
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

server_thread = threading.Thread(target=run_server)
server_thread.start()

# функція запуску боту, яка відтворює його весь час
bot.polling(none_stop=True)

server_thread.join()