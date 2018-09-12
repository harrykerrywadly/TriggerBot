#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from data.trigger import Trigger
from data_types import Type


def trigger_parse(bot, update):
    print(update)

    from utils.utils import is_valid
    if not is_valid(update):
        return

    action = update.message.reply_text
    request = update.message.text.lower()
    for trigger in Trigger.get_by_request(request):
        if trigger.type == Type.TEXT:
            action = update.message.reply_text
        elif trigger.type == Type.PHOTO:
            action = update.message.reply_photo
        elif trigger.type == Type.STICKER:
            action = update.message.reply_sticker

        action(trigger.response)
