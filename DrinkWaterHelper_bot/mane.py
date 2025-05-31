import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import random
import json
import os
from pytz import timezone
import datetime

# Токен Telegram-бота
bot = telebot.TeleBot('API TOCKEN')

# Файл для хранения подписчиков
USERS_FILE = "users.json"

# Загрузка пользователей из файла
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = f.read().strip()
                if not data:
                    return set()
                return set(json.loads(data))
        except json.JSONDecodeError:
            print("⚠️ Файл users.json повреждён или пуст. Начинаем с пустого списка.")
            return set()
    return set()

# Сохранение пользователей в файл
def save_users():
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(active_users), f)

# Инициализация подписчиков
active_users = load_users()

# Список фактов
facts = [
    "💧 Вода на Земле может быть старше самой Солнечной системы.",
    "💧 Горячая вода иногда замерзает быстрее холодной (эффект Мпемба).",
    "💧 В атмосфере Земли больше воды, чем во всех реках вместе взятых.",
    "💧 Больше воды в атмосфере, чем во всех реках мира — это подчёркивает важность гидрологического цикла."
]

# Инициализация планировщика
scheduler = BackgroundScheduler(timezone=timezone("Europe/Moscow"))

# Отправка напоминаний
def send_water_reminder():
    print(f"⏰ Напоминание. Подписчиков: {len(active_users)} — {datetime.datetime.now()}")
    for user_id in active_users:
        bot.send_message(user_id, "Напоминание — выпей стакан воды 💧")

# Планирование напоминаний (МСК: 9:00, 13:00, 18:00)
scheduler.add_job(send_water_reminder, CronTrigger(hour=8, minute=0))
scheduler.add_job(send_water_reminder, CronTrigger(hour=13, minute=0))
scheduler.add_job(send_water_reminder, CronTrigger(hour=18, minute=0))
scheduler.start()

# Команда /start
@bot.message_handler(commands=["start"])
def start_handler(message):
    user_id = message.chat.id
    if user_id in active_users:
        bot.send_message(user_id, "Ты уже подписан на напоминания 💧")
    else:
        active_users.add(user_id)
        save_users()
        bot.send_message(user_id, "Ты подписан на напоминания о воде 💧")

    # Показываем меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("/info"),
        types.KeyboardButton("/fact"),
        types.KeyboardButton("/stop")
    )
    bot.send_message(user_id, "Меню команд 👇", reply_markup=markup)

# Команда /stop
@bot.message_handler(commands=["stop"])
def stop_handler(message):
    user_id = message.chat.id
    if user_id in active_users:
        active_users.remove(user_id)
        save_users()
        bot.send_message(user_id, "Напоминания отключены ❌ Ты можешь включить их снова командой /start")
    else:
        bot.send_message(user_id, "Ты уже не подписан на напоминания 🤷‍♂️")

# Команда /info
@bot.message_handler(commands=["info"])
def info_handler(message):
    bot.send_message(message.chat.id, "Привет! Я напомню тебе пить воду 3 раза в день 🕘 🕐 🕕")

# Команда /fact
@bot.message_handler(commands=["fact"])
def fact_handler(message):
    bot.send_message(message.chat.id, random.choice(facts))

# Запуск бота
print("Бот запущен...")
bot.polling(none_stop=True)
