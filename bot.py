import sys, types
sys.modules['imghdr'] = types.ModuleType('imghdr')

import telebot
from telebot import types

# 🔑 Токен бота
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# Функция создания клавиатуры
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_info = types.KeyboardButton("ℹ️ О проекте")
    btn_news = types.KeyboardButton("🕹 Новые P2E игры")
    btn_airdrops = types.KeyboardButton("🎁 NFT Airdrop")
    btn_help = types.KeyboardButton("❓ Помощь")
    keyboard.add(btn_info, btn_news)
    keyboard.add(btn_airdrops, btn_help)
    return keyboard

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я бот по NFT и P2E-играм.\n"
        "Выбери действие из меню ниже 👇",
        reply_markup=main_menu()
    )

# Команда /info
@bot.message_handler(commands=['info'])
def info_message(message):
    bot.send_message(
        message.chat.id,
        "🎮 Здесь ты можешь узнавать:\n"
        "• Новые P2E-проекты\n"
        "• NFT-игры с наградами\n"
        "• Бесплатные airdrop'ы\n\n"
        "⚡ Нажми кнопку ниже, чтобы посмотреть последние новости.",
        reply_markup=main_menu()
    )

# Обработка кнопок
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "ℹ️ О проекте":
        bot.send_message(
            message.chat.id,
            "Этот бот создан, чтобы находить актуальные P2E и NFT проекты 💎\n"
            "Скоро появятся автоматические уведомления!"
        )
    elif message.text == "🕹 Новые P2E игры":
        bot.send_message(
            message.chat.id,
            "🎮 Примеры P2E проектов:\n"
            "• Big Time\n"
            "• Illuvium\n"
            "• Star Atlas\n"
            "• Gala Games\n\n"
            "⚡ В будущем список будет обновляться автоматически!"
        )
    elif message.text == "🎁 NFT Airdrop":
        bot.send_message(
            message.chat.id,
            "🎁 Текущие NFT Airdrop:\n"
            "• Pixels NFT — регистрация до 12 октября\n"
            "• Mythos Chain — раздача токенов MYTH\n"
            "• Animoca — готовится к запуску!\n\n"
            "💡 Проверь каждый проект перед участием."
        )
    elif message.text == "❓ Помощь":
        bot.send_message(
            message.chat.id,
            "📘 Команды:\n"
            "/start — перезапуск меню\n"
            "/info — информация о проекте\n\n"
            "Используй кнопки, чтобы выбрать категорию 👇",
            reply_markup=main_menu()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Я понимаю только команды из меню 😅",
            reply_markup=main_menu()
        )

print("🤖 Бот запущен! Ожидание сообщений...")
bot.polling(none_stop=True)
