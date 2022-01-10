import json
from pathlib import Path
import os


class MQTTConfig:

    def __get_property(self, property_name):
        data = self.__data
        property_value = data[property_name]
        return property_value

    def __init__(self):
        try:
            print("paso por 1")
            dir_path = os.path.dirname(os.path.realpath(__file__))
            data = Path(f'{dir_path}/mqtt_settings.json').read_text()
            self.errors = None
            self.__data = json.loads(data)
            self._username = self.__get_property("username")
            self._password = self.__get_property("password")
            self._id = self.__get_property("id")
            self._port = self.__get_property("port")
            self._topics = self.__get_property("topics")
            self._host = self.__get_property("host")
            topics = []

            class Topic(object):
                pass

            for t in self._topics:
                topic = Topic()
                topic.qos = t["qos"]
                topic.topic = t["topic"]
                topics.append(topic)

            self._topics = topics

        except FileNotFoundError:
            print("Configuration file mqtt_settings not found")
            self.errors = 'FileNotFound'
        except KeyError as err:
            print(
                "the key was not found in the configuration file: " + err.args[0])
            self.errors = "KeyError: " + err.args[0]
        except BaseException as err:
            print(
                f"Unexpected {err}, {type(err)} when loading the configuration")
            self.errors = 'UnexpectedError'

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def port(self):
        return self._port

    @property
    def id(self):
        return self._id

    @property
    def topics(self):
        return self._topics

    @property
    def host(self):
        return self._host
