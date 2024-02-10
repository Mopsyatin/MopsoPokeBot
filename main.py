import telebot 
from config import token
from random import randint

from logic import Pokemon, Wizard, Fighter 

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    chance = randint(1,8)
    if chance == 1:
        pokemon = Wizard(message.from_user.username)
    elif chance == 2:
        pokemon = Fighter(message.from_user.username)
    else:
        pokemon = Pokemon(message.from_user.username)
    bot.send_message(message.chat.id, pokemon.info())
    bot.send_photo(message.chat.id, pokemon.show_img())
    bot.send_message(message.chat.id, "ОСТОРОЖНО СЛЕДУЩЕЕ ИСПОЛЬЗОВАНИЕ ЭТОЙ КОМАНДЫ ПЕРЕСОЗДАСТ ВАШЕГО ПОКЕМОНА !!!БЕЗВОЗВРАТНО!!!")
    

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
            bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")

@bot.message_handler(commands=['info'])    
def info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pok.info())
        bot.send_photo(message.chat.id, pok.show_img())
    else:
        bot.reply_to(message, "У тебя еще нет покемона")

@bot.message_handler(commands=['heal'])    
def heal(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pok.heal())
    else:
        bot.reply_to(message, "У тебя еще нет покемона")

@bot.message_handler(commands=['use'])    
def use(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pok.use())
        
    else:
        bot.reply_to(message, "У тебя еще нет покемона")

@bot.message_handler(commands=['feed'])    
def levelup(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pok.level_up())
        bot.send_photo(message.chat.id, pok.show_img())
    else:
        bot.reply_to(message, "У тебя еще нет покемона")

bot.infinity_polling(none_stop=True)

