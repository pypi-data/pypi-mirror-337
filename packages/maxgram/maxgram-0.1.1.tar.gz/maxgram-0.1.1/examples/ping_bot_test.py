"""
Простой пинг-понг бот для Max

Этот бот отвечает на команду /ping сообщением "pong"
и повторяет все остальные сообщения.
"""

import asyncio
import logging
from maxgram import Bot

# Настройка логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Получение токена из переменной окружения
TOKEN = "f9LHodD0cOLxCsVYq1ooE9uDuaMrtazHuNBTkmlC8DbIrQ4hXs5UedYzgcTma3JSZHR3W_hlxwYv3ySlopom"
if not TOKEN:
    logger.error("Пожалуйста, установите переменную окружения MAX_BOT_TOKEN")
    exit(1)

# Инициализация бота
bot = Bot(TOKEN)

# Обработчик события запуска бота
@bot.on("bot_started")
def on_start(ctx):
    ctx.reply("Привет! Отправь мне ping, чтобы сыграть в пинг-понг или скажи /hello")

# Обработчик для сообщения с текстом 'ping'
@bot.hears("ping")
def ping_handler(ctx):
    ctx.reply("pong")

# Обработчик команды '/hello'
@bot.command("hello")
def hello_handler(ctx):
    ctx.reply("world")

# Обработчик для всех остальных входящих сообщений
@bot.on("message_created")
def echo(ctx):
    # Проверяем, что есть сообщение и тело сообщения
    if ctx.message and ctx.message.get("body") and "text" in ctx.message["body"]:
        # Получаем текст сообщения
        text = ctx.message["body"]["text"]
        
        # Проверяем, что это не команда и не специальные сообщения с обработчиками
        if not text.startswith("/") and text != "ping" and text != "hello":
            ctx.reply(text)

# Запуск бота
if __name__ == "__main__":
    try:
        logger.info("Запуск бота...")
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Остановка бота...")
        bot.stop()
        logger.info("Бот остановлен") 