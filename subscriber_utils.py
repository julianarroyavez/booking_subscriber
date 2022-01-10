from json import JSONEncoder
from datetime import datetime
import time


def utc2local(utc):
    epoch = time.mktime(utc.timetuple())
    offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
    return utc + offset


class JsonMessageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class JsonMessage:
    def __init__(self, box_id, messages):
        self.box_id = box_id
        self.messages = messages


urrent_utc = datetime.datetime.utcnow()
