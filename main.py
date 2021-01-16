from telebot import TeleBot, types
from random import randint

images = {
    0: "https://lh3.googleusercontent.com/proxy/tW2zNiX78Ss2v7YFmKY7bnW74JLOqFpqIUxzHLhKd1OByJupV8y_VtnkIOdLU-Yg2-2s-Stk0KUc1kDAVRE4jak5zlwFznQJIZ_ZJ43N6u6XEgFOFP-5inx61JRuFCUlGT_zhrvUu2oNY2E7qq84ljpi9Qg",
    1: "https://sun9-17.userapi.com/c849124/v849124993/2c610/vm_-aPrlZjU.jpg",
    2: "https://i.pinimg.com/originals/b6/0b/21/b60b2130ee8751b809b0427267c9e4a2.jpg",
    3: "https://forumstatic.ru/files/0007/64/ae/81080.jpg",
    4: "https://sochi.com/upload/iblock/f32/depositphotos_217531424_stock_photo_police_cars_night_police_car.jpg",
    5: "https://i2.wp.com/kurilkaeao.com/wp-content/uploads/2019/10/C8E09DA1-A055-4843-BCDB-15E62D21CBD9_4_5005_c.jpeg?fit=608%2C342&ssl=1"
}

states = {}
token = "1403032057:AAHCSKbBB1Om5-vXKvuuRcRMopb2i50s_IA"
bot = TeleBot(token)

@bot.message_handler(commands=["start"])
def start_game(message):
    user = message.chat.id

    states[user] = 0
    process_state(user, states[user])

@bot.callback_query_handler(func=lambda call: True)
def user_answer(call):
    user = call.message.chat.id
    process_answer(user, call.data)

def process_state(user, state):
    kb = types.InlineKeyboardMarkup()

    bot.send_photo(user, images[state])

    if state == 0:
        kb.add(types.InlineKeyboardButton(text="Достать фонарь", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Пойти на ощупь", callback_data="2"))

        bot.send_message(user, "Вы стоите в тёмном лесу, ничего не видно. Вы можете достать фонарь или пойти на ощупь.", reply_markup=kb)

    if state == 1:
        kb.add(types.InlineKeyboardButton(text="Постучаться", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Войти в дом без стука", callback_data="2"))

        bot.send_message(user, "Включив фонарь, вы увидели странный дом из дымохода которого идёт дым", reply_markup=kb)

    if state == 2:
        bot.send_message(user, "Вас съели волки.")
    if state == 3:
        kb.add(types.InlineKeyboardButton(text="Взять телефон и бежать", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Позвонить в полицию", callback_data="2"))

        bot.send_message(user, "Зайдя в дом вы увидели записку, лежащую на столе. В ней написано 'беги'. Рядом лежит телефон, но кто-то стучит в дверь.", reply_markup=kb)
    if state == 4:
        bot.send_message(user, "Вы убежали и спрятались за деревом. Затем вы позвонили в полицию и вас забрали")
    if state == 5:
        bot.send_message(user, "Вас убили.")

def process_answer(user, answer):
    if states[user] == 0:
        if answer == "1":
            states[user] = 1
        elif answer == "2":
            states[user] = 2

    elif states[user] == 1:
        if (answer == "2") or (answer == "1"):
            states[user] = 3
    elif states[user] == 3:
        chance = randint(0, 15)
        if (chance >= 7) and (answer == "1"):
            states[user] = 4
        elif ((chance < 7) and (answer == "1")) or (answer == "2"):
            states[user] = 5

    process_state(user, states[user])

bot.polling()