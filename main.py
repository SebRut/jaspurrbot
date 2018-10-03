#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import random
import os
import argparse
from datetime import *
from textgenrnn import textgenrnn
from dateutil import parser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import tensorflow as tf
from keras.backend import clear_session

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

global graph
clear_session()
graph = tf.get_default_graph()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

try:
    with open("VERSION") as f:
        JASPURRBOT_VERSION = f.readline()
except IOError:
    logger.warning("VERSION file doesn't exist")
    JASPURRBOT_VERSION = "don't know"

TELEGRAM_TOKEN = ""
DEFAULT_DATE = datetime.now()

argparser = argparse.ArgumentParser()
argparser.add_argument("-tgt", "--telegramtoken")
args = argparser.parse_args()

# Get telegram token
if args.telegramtoken:
    TELEGRAM_TOKEN = args.telegramtoken
if TELEGRAM_TOKEN == "":
    if "JASPURR_TG_TOKEN" in os.environ:
        TELEGRAM_TOKEN = os.environ["JASPURR_TG_TOKEN"]
    else:
        logger.error(
            "Telegram Token not provided. Ensure that your bot token is stored in JASPURR_TG_TOKEN or supplied as an "
            "argument.")
        exit(-1)

# load text generation model for jodel command
textgen = None
try:
    textgen = textgenrnn(weights_path=os.path.join('model','jodler_weights.hdf5'),
                         vocab_path=os.path.join('model','jodler_vocab.json'),
                         config_path=os.path.join('model','jodler_config.json'))
except:
    logger.error("Could not load \"jodler\" weights.")


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def miau(bot, update):
    """Echo the user message."""
    bot.sendVoice(update.message.chat_id, "AwADBAADZAMAAj-XCVFZEavNMyAhRwI")


def realmiau(bot, update):
    """Echo the user message."""
    # bot.sendVoice(update.message.chat_id, "AwADBAAD-AUAAqM3AAFRGBfdxWFEvJEC")
    bot.sendVoice(update.message.chat_id, "AwADBAADcgMAAj-XCVFePU9mLhwqowI")


def gadse(bot, update):
    bot.sendSticker(update.message.chat_id, "CAADAgADIgADCDNuC_W1EzQvQ_GeAg")


def agent(bot, update):
    bot.sendSticker(update.message.chat_id, "CAADAgADJgADCDNuC2KkEJNZMbn6Ag")


def cheers(bot, update):
    bot.sendSticker(update.message.chat.id, "CAADAgADIwADCDNuC1qjnMjwLZ-OAg")


def version(bot, update):
    bot.sendMessage(update.message.chat_id, JASPURRBOT_VERSION)


def error(_, update, i):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, i)


def check_for_time(bot, update):
    try:
        n_time = parser.parse(update.message.text, default=DEFAULT_DATE, fuzzy=True)
        j_time = to_jasper_time(n_time)
        message = "{} entspricht {} in Jasperzeit".format(n_time.strftime("%H:%M Uhr am %d.%m.%Y"),
                                                          j_time.strftime("%H:%M Uhr am %d.%m.%Y"))
        bot.sendMessage(update.message.chat_id, message)
    except ValueError:
        pass


def to_jasper_time(n_time):
    j_time = n_time + timedelta(minutes=random.randint(10, 30))
    return j_time


def jtime(bot, update):
    message = "Zeitformat unbekannt!"
    try:
        command = update.message.text
        n_time = parser.parse(command[command.find(' '):], default=DEFAULT_DATE, fuzzy=True)
        j_time = to_jasper_time(n_time)
        message = "{} entspricht {} in Jasperzeit".format(n_time.strftime("%H:%M Uhr am %d.%m.%Y"),
                                                          j_time.strftime("%H:%M Uhr am %d.%m.%Y"))
    except ValueError:
        pass

    bot.sendMessage(update.message.chat_id, message)


def file_received(_, update):
    print(update.message)


def jodel(bot, update):
    """Generate a Jodel."""
    if textgen is not None:
        with graph.as_default():
            message = textgen.generate(1, return_as_list=True)[0]
    else:
        message = "I han k1 Jodel-Diplom :("
    bot.sendMessage(update.message.chat_id, message)

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
    dp.add_handler(CommandHandler("jodel", jodel))
    dp.add_handler(CommandHandler("jr600", agent))
    dp.add_handler(CommandHandler("cheers", cheers))
    dp.add_handler(CommandHandler("version", version))

    # log all errors
    dp.add_error_handler(error)

    # handle received files
    dp.add_handler(MessageHandler(Filters.voice
                                  | Filters.audio
                                  | Filters.contact
                                  | Filters.document
                                  | Filters.photo
                                  | Filters.sticker
                                  | Filters.video, file_received))

    dp.add_handler(MessageHandler(Filters.text, check_for_time))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
