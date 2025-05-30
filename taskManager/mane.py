import telebot
from telebot import types
import json
from datetime import datetime
import os

bot = telebot.TeleBot("7444456257:AAFnxtKc839wDlTBoGw3dOxwy9_mJAP8jU0")
TASK_FILE = "tasks.json"
tasks = []

# === КЛАСС ЗАДАЧИ ===
class Task:
    def __init__(self, description, deadline, completed=False):
        self.description = description
        self.deadline = deadline
        self.completed = completed

    def mark_done(self):
        self.completed = True

    def to_dict(self):
        return {
            "description": self.description,
            "deadline": self.deadline,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(data["description"], data["deadline"], data["completed"])

    def __str__(self):
        status = "✅" if self.completed else "❌"
        return f"{status} {self.description} (до {self.deadline})"


# === ЗАГРУЗКА / СОХРАНЕНИЕ ===
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Task.from_dict(d) for d in data]
    return []

def save_tasks():
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tasks], f, ensure_ascii=False, indent=2)

# Загрузим существующие задачи
tasks = load_tasks()


# === ОБРАБОТКА КОМАНД ===
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("/add", "/list", "/done", "/store", "/help")
    bot.send_message(message.chat.id, "Привет! Это бот-менеджер задач и товаров 🧾", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, "/add — добавить задачу\n/list — список\n/done — отметить задачу выполненной\n/store — пример работы с магазинами")

@bot.message_handler(commands=['add'])
def add_task(message):
    msg = bot.send_message(message.chat.id, "Введите задачу в формате: `Описание | ДД.ММ.ГГГГ`", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_task_input)

def process_task_input(message):
    try:
        description, date_str = map(str.strip, message.text.split('|'))
        datetime.strptime(date_str, "%d.%m.%Y")  # проверим корректность
        task = Task(description, date_str)
        tasks.append(task)
        save_tasks()
        bot.send_message(message.chat.id, "✅ Задача добавлена!")
    except:
        bot.send_message(message.chat.id, "⚠ Неверный формат. Попробуйте снова: /add")

@bot.message_handler(commands=['list'])
def list_tasks(message):
    not_done = [str(t) for t in tasks if not t.completed]
    if not not_done:
        bot.send_message(message.chat.id, "🎉 Все задачи выполнены!")
    else:
        msg = "\n".join(f"{i+1}. {t}" for i, t in enumerate(not_done))
        bot.send_message(message.chat.id, f"📋 Невыполненные задачи:\n\n{msg}")

@bot.message_handler(commands=['done'])
def done_task(message):
    not_done = [t for t in tasks if not t.completed]
    if not not_done:
        bot.send_message(message.chat.id, "Нет задач для завершения.")
        return
    msg = "\n".join(f"{i+1}. {t.description}" for i, t in enumerate(not_done))
    msg += "\n\nВведите номер задачи, которую хотите завершить:"
    sent = bot.send_message(message.chat.id, msg)
    bot.register_next_step_handler(sent, process_done)

def process_done(message):
    try:
        index = int(message.text) - 1
        not_done = [t for t in tasks if not t.completed]
        if 0 <= index < len(not_done):
            not_done[index].mark_done()
            save_tasks()
            bot.send_message(message.chat.id, "✅ Задача завершена!")
        else:
            bot.send_message(message.chat.id, "Неверный номер.")
    except:
        bot.send_message(message.chat.id, "⚠ Введите корректный номер.")


# === КЛАСС МАГАЗИНА ===
class Store:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.items = {}

    def add_item(self, name, price):
        self.items[name] = price

    def remove_item(self, name):
        self.items.pop(name, None)

    def get_price(self, name):
        return self.items.get(name)

    def update_price(self, name, new_price):
        if name in self.items:
            self.items[name] = new_price

    def __str__(self):
        return f"{self.name} ({self.address})\nТовары: {self.items}"


@bot.message_handler(commands=["store"])
def store_example(message):
    store = Store("Фрукты и Ягоды", "ул. Садовая, 12")
    store.add_item("Яблоки", 0.5)
    store.add_item("Вишня", 1.2)
    store.update_price("Яблоки", 0.55)
    store.remove_item("Вишня")
    reply = str(store)
    bot.send_message(message.chat.id, f"Пример магазина:\n\n{reply}")


bot.polling(none_stop=True)
