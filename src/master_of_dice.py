
import logging
from telegram.ext import Updater
updater = Updater(token='TOKEN', use_context=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

dispatcher = updater.dispatcher

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)