#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Capybara Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
import pymysql
import logging

from config import DB


class DataBase:
    @staticmethod
    def get_connection():
        connection = pymysql.connect(
            cursorclass=pymysql.cursors.DictCursor, **DB)

        return connection

    @staticmethod
    def query(query, args=None, fetch=False, list=False):
        connection = DataBase.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, args)

                if fetch:
                    result = cursor.fetchall()

                    if list:
                        return result

                    if len(result) == 1:
                        return result[0]
                    else:
                        return result

            connection.commit()
        except pymysql.MySQLError as e:
            logging.error(e)
        finally:
            connection.close()
