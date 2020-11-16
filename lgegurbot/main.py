'''
Main
'''
import os
import logging
import argparse
# from flask import Flask, request, json
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# from telegram.ext import dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
log = logging.getLogger(__name__)

def parse_args():
    '''
    Argument parser
    '''
    parser = argparse.ArgumentParser(description='Lgegurbot')
    log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
    parser.add_argument(
        "--log_level", default=log_level,
        help="Log level. CRITICAL|ERROR|WARNING|INFO|DEBUG|NOTSET,"
        " read more: https://docs.python.org/3/library/logging.html#levels"
    )
    
    parser.add_argument(
        "-c", "--config", default="./.gitlab-ci/yt_magic.yml",
        help="Path to config file"
    )
    
    parser.add_argument(
        "-t", "--token",
        required=True,
        help="Telegram token from BotFather"
    )
    parser.add_argument(
        "--chat-id",
        required=True,
        help="Telegram chat ID"
    )
    
    return parser.parse_args()

def text_message(update: Update, context: CallbackContext):
    """
    This function reads text and replies on it
    """
    user = update.message.from_user
    print(update)
    response = 'Получил Ваше сообщение: ' + update.message.text
    update.message.reply_text(response)
    log.info("Received message '%s' from %s in %s", update.message.text, user.username, update.message.chat_id)

def error(update, error):
    """Log Errors caused by Updates."""
    log.warning('Update "%s" caused error "%s"', update, error)

def main():
    '''
    Main entrypoint
    '''
    args = parse_args()

    # bot = telegram.Bot(token=args.token)
    # print(bot.get_me())
    # updater = bot.getUpdates()

    updater = Updater(token=args.token) 
    dispatcher = updater.dispatcher
    text_message_handler = MessageHandler(Filters.all, text_message)
    dispatcher.add_handler(text_message_handler)
    dispatcher.add_error_handler(error)

    updater.start_polling(clean=True)

    updater.idle()

    # members = bot.getChatMembersCount(args.chat_id)
    # print(members)

    # print(*bot.getChatAdministrators(args.chat_id))

if __name__ == "__main__":
    main()

