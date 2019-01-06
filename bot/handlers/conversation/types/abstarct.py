# encoding: utf-8
from __future__ import unicode_literals

from default_logger import logger


class ConversationType(object):
    """"""
    def __init__(self):
        self.logger = logger

    @property
    def entry_points(self):
        return NotImplemented

    @property
    def states(self):
        return NotImplemented
