from configuration import BookingSubscriberConfiguration
from mqtt.mqtt_config import MQTTConfig
from data.ev_charger_db import EvChargerDb
from subscriber_client import BookingSubscriberClient


def run_subscriber():
    mqtt_config = MQTTConfig()
    booking_subscriber_config = BookingSubscriberConfiguration()
    if mqtt_config.errors:
        print("Exiting program, errors found: " + mqtt_config.errors)
        exit(1)
    ev_charger_db = EvChargerDb(booking_subscriber_config.ev_db_path)
    mqtt_client = BookingSubscriberClient(mqtt_config, booking_subscriber_config, ev_charger_db)
    if mqtt_client:
        try:
            mqtt_client.listen()
            print("Exiting")
        except BaseException as err:
            print(
                f"Unexpected {err}, {type(err)} when connecting to mqtt server")
            raise
        finally:
            mqtt_client.client.disconnect()


if __name__ == '__main__':
    run_subscriber()
