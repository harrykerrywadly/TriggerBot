#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from data.trigger import Trigger


def triggers_list(bot, update):
    from utils.utils import is_valid
    if not is_valid(update, admin=True):
        return

    text = 'List of existing triggers: \n'
    for enabled_trigger in Trigger.get_all_enabled():
        text += '{} - номер: {}\n'.format(enabled_trigger.request, enabled_trigger.id)

    update.message.reply_text(text)
