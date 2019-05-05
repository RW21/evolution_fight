from monster import BaseMonster


class Traits:
    def __init__(self, body_part, value):
        self.dominant = False
        self.body_part = body_part
        self.value = value

    def __set__(self, instance, value):
        instance.gene




