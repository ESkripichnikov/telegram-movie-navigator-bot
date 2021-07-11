import logging
from aiogram import Bot, Dispatcher, executor
from callbacks.callbacks import register_callbacks
from config import bot_token
from message_handlers import register_handlers


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot)

register_handlers(dispatcher)
register_callbacks(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
