#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Capybara Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
import logging

from config import telegram_token
from database import DataBase as db

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def is_valid(update, admin=False):
    if update.message.chat.type != 'supergroup':
        return False
    if admin and updater.bot.get_chat_member(update.message.chat.id, update.message.from_user.id).status == 'member':
        return False

    return True


def trigger_list(bot, update):
    if not is_valid(update, admin=True):
        return

    triggers = db.query(
        "SELECT * FROM `triggers`", fetch=True, list=True
    )

    text = 'List of triggers: \n'
    for trigger in triggers:
        text += '"{}"; ID: {}\n'.format(trigger['response'], trigger['id'])

    update.message.reply_text(text)


def trigger_add_step_1(bot, update, args):
    if not is_valid(update, admin=True):
        return

    request = ' '.join(args)

    if not request:
        update.message.reply_text('Where request?')

        return

    addition_process.update({update.message.from_user.id: request})

    update.message.reply_text(
        'Trigger: "{}"\n/trigger_cancel to revoke \n\nSet the sticker/photo/text to response of trigger:'.format(request)
    )


def trigger_add_step_2(bot, update):
    trigger_type = trigger_response = None
    trigger_request = addition_process.get(update.message.from_user.id)

    if trigger_request is None:
        return

    attachment = update.message.effective_attachment
    if isinstance(attachment, telegram.Sticker):
        trigger_type = 'sticker'
        trigger_response = update.message.sticker.file_id
    elif isinstance(attachment, list):
        trigger_type = 'photo'
        trigger_response = update.message.photo[0].file_id
    elif not attachment and not update.message.entities:
        trigger_type = 'text'
        trigger_response = update.message.text
    elif not attachment:
        trigger_type = 'command'

    if trigger_type and trigger_type != 'command':
        db.query(
            "INSERT INTO `triggers` (`request`, `response`, `type`) VALUES (%s, %s, %s)",
            (trigger_request.lower(), trigger_response, trigger_type)
        )

        addition_process.pop(update.message.from_user.id)
        update.message.reply_text('Successfully added')
    elif trigger_type != 'command':
        update.message.reply_text('Incorrect type. One more try:')


def trigger_cancel(bot, update):
    if addition_process.get(update.message.from_user.id) is not None:
        addition_process.pop(update.message.from_user.id)

        update.message.reply_text('Successfully revoked')


def trigger_delete(bot, update, args):
    if not is_valid(update, admin=True):
        return

    if not args:
        update.message.reply_text("Where ID?")

        return

    trigger = db.query(
        "SELECT * FROM `triggers` WHERE `id` = %s", args[0], fetch=True
    )

    if not trigger:
        update.message.reply_text('Cant\'n find trigger with ID = {}'.format(args[0]))
    else:
        db.query(
            "DELETE FROM `triggers` WHERE `id` = %s", args[0]
        )

        update.message.reply_text('Successfully deleted')


def trigger(bot, update):
    if not is_valid(update):
        return

    prepared_message = update.message.text.lower()
    responses = db.query(
        "SELECT * FROM `triggers` WHERE `request`=%s",
        prepared_message, fetch=True, list=True
    )

    if not responses:
        return

    for response in responses:
        if response['type'] == 'text':
            update.message.reply_text(response['response'])
        elif response['type'] == 'photo':
            update.message.reply_photo(response['response'])
        elif response['type'] == 'sticker':
            update.message.reply_sticker(response['response'])


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == '__main__':
    addition_process = {}
    updater = Updater(telegram_token)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, trigger))

    dp.add_handler(CommandHandler(['triggers', 'tr', 'trl'], trigger_list))
    dp.add_handler(CommandHandler(['trigger_delete', 'trigger_del', 'trd'], trigger_delete, pass_args=True))

    dp.add_handler(CommandHandler(['trigger_cancel', 'trc'], trigger_cancel))
    dp.add_handler(CommandHandler(['trigger_add', 'tra'], trigger_add_step_1, pass_args=True))
    dp.add_handler(MessageHandler(Filters.all, trigger_add_step_2), group=1)

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
