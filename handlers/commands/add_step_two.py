#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
import telegram

from data_types import Type


def trigger_add_step_two(bot, update):
    from main import Bot
    new_trigger = Bot.addition_process.get(update.message.from_user.id)

    if new_trigger is None:
        return

    _type = response = None
    attachment = update.message.effective_attachment
    if isinstance(attachment, telegram.Sticker):
        _type = Type.STICKER
        response = update.message.sticker.file_id
    elif isinstance(attachment, list):
        _type = Type.PHOTO
        response = update.message.photo[0].file_id
    elif not attachment:
        _type = Type.TEXT
        response = update.message.text

    if _type:
        new_trigger.response = response
        new_trigger.type = _type

        new_trigger.save()

        Bot.addition_process.pop(update.message.from_user.id)
        update.message.reply_text('Trigger was successfully created!')
    else:
        update.message.reply_text('This cannot be used as a response to a trigger. try again:')
