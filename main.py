#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import random
import os
import argparse
from datetime import *

from dateutil import parser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_TOKEN = ""
DEFAULT_DATE = datetime.now()

argparser = argparse.ArgumentParser()
argparser.add_argument("-tgt", "--telegramtoken")
args = argparser.parse_args()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Get telegram token
if args.telegramtoken:
    TELEGRAM_TOKEN = args.telegramtoken
if TELEGRAM_TOKEN == "":
    if "JASPURR_TG_TOKEN" in os.environ:
        TELEGRAM_TOKEN = os.environ["JASPURR_TG_TOKEN"]
    else:
        logger.error("Telegram Token not provided. Ensure that your bot token is stored in JASPURR_TG_TOKEN or supplied as an argument.")
        exit(-1)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def miau(bot, update):
    """Echo the user message."""
    bot.sendVoice(update.message.chat_id, "AwADBAADZAMAAj-XCVFZEavNMyAhRwI")


def realmiau(bot, update):
    """Echo the user message."""
    #bot.sendVoice(update.message.chat_id, "AwADBAAD-AUAAqM3AAFRGBfdxWFEvJEC")
    bot.sendVoice(update.message.chat_id, "AwADBAADcgMAAj-XCVFePU9mLhwqowI")


def gadse(bot, update):
    bot.sendSticker(update.message.chat_id, "CAADAgADIgADCDNuC_W1EzQvQ_GeAg")


def agent(bot, update):
    bot.sendSticker(update.message.chat_id, "CAADAgADJgADCDNuC2KkEJNZMbn6Ag")


def cheers(bot, update):
    bot.sendSticker(update.message.chat.id, "CAADAgADIwADCDNuC1qjnMjwLZ-OAg")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def check_for_time(bot, update):
    try:
        ntime = parser.parse(update.message.text, default=DEFAULT_DATE, fuzzy=True)
        jtime = to_jasper_time(ntime)
        message = "{} entspricht {} in Jasperzeit".format(ntime.strftime("%H:%M Uhr am %d.%m.%Y"),
                                                          jtime.strftime("%H:%M Uhr am %d.%m.%Y"))
        bot.sendMessage(update.message.chat_id, message)
    except ValueError:
        pass


def to_jasper_time(ntime):
    jtime = ntime + timedelta(minutes=random.randint(10, 30))
    return jtime


def jtime(bot, update):
    message = "Zeitformat unbekannt!"
    try:
        command = update.message.text
        ntime = parser.parse(command[command.find(' '):], default=DEFAULT_DATE, fuzzy=True)
        jtime = to_jasper_time(ntime)
        message = "{} entspricht {} in Jasperzeit".format(ntime.strftime("%H:%M Uhr am %d.%m.%Y"),
                                                          jtime.strftime("%H:%M Uhr am %d.%m.%Y"))
    except ValueError:
        pass

    bot.sendMessage(update.message.chat_id, message)


def file_received(bot, update):
    print(update.message)


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("miau", miau))
    dp.add_handler(CommandHandler("realmiau", realmiau))
    dp.add_handler(CommandHandler("gadse", gadse))
    dp.add_handler(CommandHandler("jasperzeit", jtime))
    dp.add_handler(CommandHandler("jr600", agent))
    dp.add_handler(CommandHandler("cheers", cheers))

    # log all errors
    dp.add_error_handler(error)

    dp.add_handler(MessageHandler(Filters.voice, file_received))
    dp.add_handler(MessageHandler(Filters.audio, file_received))
    dp.add_handler(MessageHandler(Filters.contact, file_received))
    dp.add_handler(MessageHandler(Filters.document, file_received))
    dp.add_handler(MessageHandler(Filters.photo, file_received))
    dp.add_handler(MessageHandler(Filters.sticker, file_received))
    dp.add_handler(MessageHandler(Filters.video, file_received))

    dp.add_handler(MessageHandler(Filters.text, check_for_time))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
