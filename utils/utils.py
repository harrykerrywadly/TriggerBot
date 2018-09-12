#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from main import Bot


def is_valid(update, admin=False):
    if update.message.chat.type != 'supergroup':
        return False
    if admin and Bot.updater.bot.get_chat_member(update.message.chat.id, update.message.from_user.id).status == 'member':
        return False

    return True
