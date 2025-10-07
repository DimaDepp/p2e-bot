import telebot
from telebot import types
import requests

# 🔑 Токен бота
BOT_TOKEN = "8319750794:AAEA6sRL5F-BK0we8ar0SCuJY96Mbcijof4"

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

# --- Команда /start ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я бот для мониторинга P2E/NFT проектов.\n\nВыбери действие:",
        reply_markup=main_menu()
    )

# --- Команда /info ---
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ Здесь ты можешь получать новости о P2E-играх и NFT airdrop.\n⚡ В будущем список проектов будет обновляться автоматически.",
        reply_markup=main_menu()
    )

# --- Получение списка проектов (пример через CoinGecko API) ---
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

# --- Обработка нажатий кнопок ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    if "инфо" in text:
        bot.send_message(message.chat.id, "📘 Этот бот мониторит новые P2E и NFT проекты. Используй кнопки ниже для просмотра.", reply_markup=main_menu())
    elif "новые p2e игры" in text:
        bot.send_message(message.chat.id, "🎮 Последние P2E проекты:\n\n" + get_projects())
    elif "nft airdrop" in text:
        bot.send_message(message.chat.id, "🎁 Примеры текущих NFT Airdrop:\n- Pixels NFT\n- Mythos Chain\n- Animoca", reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "❓ Не понимаю команду. Выбери действие из меню.", reply_markup=main_menu())

print("✅ P2E/NFT бот запущен и работает 24/7 на Render...")
bot.polling(none_stop=True)
