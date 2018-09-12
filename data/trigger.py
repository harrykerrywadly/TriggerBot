#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from utils.database import DataBase as db
from data_types import Type


class Trigger(object):
    def __init__(self, trigger_data=None, request=None, response=None, _type='text', enable=True):
        if trigger_data:
            self.id = trigger_data['id']
            self.request = trigger_data['request']
            self.response = trigger_data['response']
            self.type = Type(trigger_data['type'])
            self.enable = trigger_data['enable']
        else:
            self.id = None
            self.request = request.lower()
            self.response = response
            self.type = Type(_type)
            self.enable = enable

    def save(self):
        if self.id:
            db.query(
                "UPDATE `triggers` SET `request` = %s, `response` = %s, `type` = %s, `enable` = %s WHERE `id` = %s",
                (self.request, self.response, self.type, self.enable, self.id)
            )
        else:
            db.query(
                "INSERT INTO `triggers` (`request`, `response`, `type`) VALUES (%s, %s, %s)",
                (self.request, self.response, self.type)
            )

            self.id = db.query(
                "SELECT `id` FROM `triggers` WHERE `request` = %s ORDER BY `id` DESC LIMIT 1",
                self.request, fetch=True
            )['id']

    @staticmethod
    def get_by_request(request):
        result = db.query(
            "SELECT * FROM `triggers` WHERE `enable` = True and `request` = %s",
            request, fetch=True, as_list=True
        )

        triggers = list(map(Trigger, result))
        return triggers

    @staticmethod
    def get_by_id(_id):
        result = db.query(
            "SELECT * FROM `triggers` WHERE `enable` = True and `id` = %s",
            _id, fetch=True
        )

        if result:
            return Trigger(result)
        else:
            return None

    @staticmethod
    def get_all_enabled():
        result = db.query(
            "SELECT * FROM `triggers` WHERE `enable` = True", fetch=True, as_list=True
        )

        triggers = list(map(Trigger, result))
        return triggers
