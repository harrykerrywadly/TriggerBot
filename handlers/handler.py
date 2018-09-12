#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pepkobot Copyright © 2018 Il'ya Marshal Semyonov
# License: https://www.gnu.org/licenses/gpl-3.0.en.html
from enum import Enum

from handlers.commands.list import triggers_list
from handlers.commands.delete import trigger_delete
from handlers.commands.add_step_one import trigger_add_step_one
from handlers.commands.add_step_two import trigger_add_step_two
from handlers.commands.add_cancel import trigger_add_cancel

from handlers.trigger_parse import trigger_parse


class Handler(Enum):
    LIST = triggers_list
    DELETE = trigger_delete
    ADD_STEP_ONE = trigger_add_step_one
    ADD_STEP_TWO = trigger_add_step_two
    ADD_CANCEL = trigger_add_cancel
    PARSE = trigger_parse
