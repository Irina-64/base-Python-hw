import telebot
import datetime
import time
import threading
import random

bot = telebot.TeleBot('8179812229:AAE_5nLhL0N5waWFsgakivhDyBRHdaX1-0s')

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.reply_to(message, 'Привет! я чат-бот, который будет напоминать тебе пить воду')
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()

@bot.message_handler(commands=["fact"])
def fact_message(message):
    list = ["**Вода на Земле может быть старше самой Солнечной системы**: Исследования показывают, что от 30% до 50% воды в наших океанах возможно присутствовала в межзвездном пространстве еще до формирования Солнечной системы около 4,6 миллиарда лет назад.",
"**Горячая вода замерзает быстрее холодной**: Это явление известно как эффект Мпемба. Под определенными условиями горячая вода может замерзать быстрее, чем холодная, хотя ученые до сих пор полностью не разгадали механизм этого процесса.",
"**Больше воды в атмосфере, чем во всех реках мира**: Объем водяного пара в атмосфере Земли в любой момент времени превышает объем воды во всех реках мира вместе взятых. Это подчеркивает важную роль атмосферы в гидрологическом цикле, перераспределяя воду по планете."]
    random_fact = random.choice(list)
    bot.reply_to(message, f'Лови факт о воде {random_fact}')

def send_reminders(chat_id):
    first_rem = "01:37"
    second_rem = "01:38"
    end_rem = "18:00"
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == first_rem:
            bot.send_message(chat_id, "Напоминание - выпей первый стакан воды")
            time.sleep(60)
        elif now == second_rem:
            bot.send_message(chat_id, "Напоминание - выпей второй стакан воды")
            time.sleep(60)
        elif now == end_rem:
            bot.send_message(chat_id, "Напоминание - выпей третий стакан воды")
            time.sleep(60)
        time.sleep(1)

bot.polling(none_stop=True)