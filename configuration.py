import json
from pathlib import Path
import os


class BookingSubscriberConfiguration:

    def __get_property(self, property_name):
        data = self.__data
        property_value = data[property_name]
        return property_value

    def __init__(self):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            data = Path(f'{dir_path}/settings.json').read_text()
            self.errors = None
            self.__data = json.loads(data)
            self._hygge_box_number = self.__get_property("hygge_box_number")
            self._station_id = self.__get_property("station_id")
            self._charger_point_id = self.__get_property("charger_point_id")
            self._ev_db_path = self.__get_property("ev_db_path")

            

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
    def hygge_box_number(self):
        return self._hygge_box_number

    @property
    def station_id(self):
        return self._station_id

    @property
    def charger_point_id(self):
        return self._charger_point_id

    @property
    def ev_db_path(self):
        return self._ev_db_path

        