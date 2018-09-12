#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
import logging

from config import telegram_token
# from localConfig import telegram_token
from handlers.handler import Handler

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Bot(object):
    updater = Updater(telegram_token)
    dispatcher = updater.dispatcher
    addition_process = {}

    def __init__(self):
        Bot.register_handlers()
        Bot.register_error_handler()

    @staticmethod
    def start():
        Bot.updater.start_polling()
        Bot.updater.idle()

    @staticmethod
    def register_handlers():
        Bot.dispatcher.add_handler(MessageHandler(Filters.text, Handler.PARSE))
        Bot.dispatcher.add_handler(CommandHandler(['trl'], Handler.LIST))
        Bot.dispatcher.add_handler(CommandHandler(['trd'], Handler.DELETE, pass_args=True))

        Bot.dispatcher.add_handler(CommandHandler(['trc'], Handler.ADD_CANCEL), group=1)
        Bot.dispatcher.add_handler(CommandHandler(['tra'], Handler.ADD_STEP_ONE, pass_args=True), group=1)
        Bot.dispatcher.add_handler(MessageHandler(Filters.all, Handler.ADD_STEP_TWO), group=1)

    @staticmethod
    def register_error_handler():
        Bot.dispatcher.add_error_handler(Bot.error)

    @staticmethod
    def error(bot, update, error):
        logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    Bot().start()
