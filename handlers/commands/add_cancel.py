#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html


def trigger_add_cancel(bot, update):
    from main import Bot
    if Bot.addition_process.get(update.message.from_user.id) is not None:
        Bot.addition_process.pop(update.message.from_user.id)

        update.message.reply_text('Создание отменено...')
