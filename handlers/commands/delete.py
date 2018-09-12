#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from data.trigger import Trigger


def trigger_delete(bot, update, args):
    from utils.utils import is_valid
    if not is_valid(update, admin=True):
        return

    if not args:
        update.message.reply_text("/trd <номер триггера>")
        return

    trigger = Trigger.get_by_id(args[0])
    if not trigger:
        update.message.reply_text('Не могу найти триггер с номером {}'.format(args[0]))
    else:
        trigger.enable = False
        trigger.save()

        update.message.reply_text('Триггер удалён')
