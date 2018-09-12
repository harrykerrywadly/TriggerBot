from enum import Enum


class Type(Enum):
    TEXT = 'text'
    PHOTO = 'photo'
    STICKER = 'sticker'

    def __str__(self):
        return self.value
