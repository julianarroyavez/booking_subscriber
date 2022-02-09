import json
from pathlib import Path
from cryptography.fernet import Fernet


class MqttConfiguration:
    pass


class BookingSubscriberConfiguration:
    def __get_mqtt_config(self, mqtt_data, subscriber_config):
        mqtt = MqttConfiguration()
        mqtt.username = self.__get_property("username", mqtt_data)
        mqtt.password = self.__get_property("password", mqtt_data)

        key = "hyggeenergyhyggeenergyhyggeenergy1234123123="
        fernet = Fernet(key.encode())

        mqtt.password = fernet.decrypt(mqtt.password.encode()).decode()

        mqtt.id = self.__get_property("subscriber_id", subscriber_config)
        mqtt.port = self.__get_property("port", mqtt_data)
        mqtt.host = self.__get_property("host", mqtt_data)
        mqtt.topics = self.__get_property("topics", subscriber_config)
        topics = []

        class Topic(object):
            pass

        for t in mqtt.topics:
            topic = Topic()
            topic.qos = t["qos"]
            topic.topic = t["topic"]
            topics.append(topic)

            mqtt.topics = topics

        return mqtt

    def __get_property(self, property_name, data=None):
        if data is None:
            data = self.__data
        property_value = data[property_name]
        return property_value

    def __init__(self):
        try:
            dir_file = "/home/pi/settings.json"
            self.errors = None
            data = Path(dir_file).read_text()
            self.__data = json.loads(data)
            subscriber_config = self.__get_property("booking_subscriber")
            mqtt_config = self.__get_property("mqtt")

            self.mqtt = self.__get_mqtt_config(mqtt_config, subscriber_config)
            self._station_id = self.__get_property("station_id", subscriber_config)
            self._charger_point_id = self.__get_property("charger_point_id", subscriber_config)
            self._ev_db_path = self.__get_property("project_db_path", self.__data)
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
    def station_id(self):
        return self._station_id

    @property
    def charger_point_id(self):
        return self._charger_point_id

    @property
    def ev_db_path(self):
        return self._ev_db_path
