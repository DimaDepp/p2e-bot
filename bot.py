import telebot
from telebot import types
import requests
from flask import Flask, request
import os
from auto_fetch import fetch_new_p2e


# 🔑 Токен бота через переменные окружения (рекомендуется)
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# --- Главное меню ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("ℹ️ Инфо"),
        types.KeyboardButton("🎮 Новые P2E игры"),
        types.KeyboardButton("🎁 NFT Airdrop")
    )
    return markup

# --- Команды ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я бот для мониторинга P2E/NFT проектов.\n\nВыбери действие:",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ Здесь ты можешь получать новости о P2E-играх и NFT airdrop.\n⚡ Список проектов обновляется автоматически.",
        reply_markup=main_menu()
    )

# --- Получение списка проектов через CoinGecko ---
def get_projects():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "category": "play-to-earn",
            "order": "market_cap_desc",
            "per_page": 5,
            "page": 1,
            "sparkline": "false"
        }
        response = requests.get(url, params=params)
        data = response.json()
        projects = []
        for p in data:
            projects.append(f"{p['name']} ({p['symbol'].upper()}): ${p['current_price']}\nПодробнее: https://www.coingecko.com/en/coins/{p['id']}")
        return "\n\n".join(projects)
    except Exception as e:
        return f"Ошибка при получении проектов: {e}"

# --- Обработка кнопок ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if "инфо" in text:
        bot.send_message(message.chat.id, "📘 Этот бот мониторит P2E/NFT проекты. Используй кнопки ниже для просмотра.", reply_markup=main_menu())
    elif "новые p2e игры" in text:
        bot.send_message(message.chat.id, "🎮 Последние P2E проекты:\n\n" + get_projects())
    elif "nft airdrop" in text:
        bot.send_message(message.chat.id, "🎁 Примеры текущих NFT Airdrop:\n- Pixels NFT\n- Mythos Chain\n- Animoca", reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "❓ Не понимаю команду. Выбери действие из меню.", reply_markup=main_menu())

# --- Flask для Webhook ---
app = Flask(__name__)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Укажи URL сервиса Render

# Настройка Webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

@app.route("/", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    # Запуск Flask на Render
    app.run(host="0.0.0.0", port=10000)
    
    @bot.message_handler(commands=['autogames'])
def autogames_cmd(message):
    bot.send_chat_action(message.chat.id, 'typing')
    games = fetch_new_p2e(limit=5)
    if not games:
        bot.reply_to(message, "😕 Не удалось получить новые проекты.")
        return
    text = "🎯 *Автоматический поиск P2E-проектов:*\n\n"
    for g in games:
        text += f"🎮 *{g['name']}*\n🗂 {g['genre']}\n🔗 {g['link']}\n\n"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

