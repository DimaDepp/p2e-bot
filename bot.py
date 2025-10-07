import os
import logging
import telebot
from flask import Flask, request, abort

# Импорт обработчиков
from handlers.start_handler import register_start_handler
from handlers.about_handler import register_about_handler
from handlers.newgames_handler import register_newgames_handler
from handlers.airdrops_handler import register_airdrops_handler

# Импорт нового модуля автоматического поиска
from auto_fetch import fetch_new_p2e

# Настройки логирования
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("p2e-bot")

# --- Загружаем секреты из Environment ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")

if not BOT_TOKEN or not WEBHOOK_URL or not WEBHOOK_PATH:
    raise ValueError("Не заданы BOT_TOKEN, WEBHOOK_URL или WEBHOOK_PATH в Render Environment")

WEBHOOK_URL = WEBHOOK_URL.rstrip('/')
WEBHOOK_ENDPOINT = f"/webhook/{WEBHOOK_PATH}"
FULL_WEBHOOK_URL = f"{WEBHOOK_URL}{WEBHOOK_ENDPOINT}"

# --- Инициализация бота ---
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- Регистрируем старые обработчики ---
register_start_handler(bot)
register_about_handler(bot)
register_newgames_handler(bot)
register_airdrops_handler(bot)

# --- Новый обработчик команды /autogames ---
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

# --- Flask endpoint для webhook ---
@app.route(WEBHOOK_ENDPOINT, methods=['POST'])
def webhook_handler():
    if request.headers.get('content-type') != 'application/json':
        return abort(400)
    update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
    bot.process_new_updates([update])
    return '', 200

# --- Установка webhook ---
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=FULL_WEBHOOK_URL)
    log.info(f"Webhook установлен: {FULL_WEBHOOK_URL}")

# --- Запуск Flask ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    set_webhook()
    app.run(host="0.0.0.0", port=port)

