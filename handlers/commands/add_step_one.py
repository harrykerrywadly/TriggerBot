#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from data.trigger import Trigger


def trigger_add_step_one(bot, update, args):
    from utils.utils import is_valid
    from main import Bot
    if not is_valid(update, admin=True):
        return

    request = ' '.join(args)
    if not request:
        update.message.reply_text('/tda <текст триггера>')
        return

    Bot.addition_process.update({update.message.from_user.id: Trigger(request=request)})

    update.message.reply_text('/tdc - отмена создания\n\nОтправьте ответ на триггер:')
