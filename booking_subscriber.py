import logging
import sys
from pathlib import Path
from configuration import BookingSubscriberConfiguration
from data.ev_charger_db import EvChargerDb
from subscriber_client import BookingSubscriberClient


def run_subscriber():
    config_path = str(Path.home()) + "/settings.ini"
    for i, arg in enumerate(sys.argv):
        if arg == "-config":
            config_path = sys.argv[i + 1]
            break
    config = BookingSubscriberConfiguration(config_path)

    ev_charger_db = EvChargerDb(config.project_db_path)
    mqtt_client = BookingSubscriberClient(config, ev_charger_db)
    if mqtt_client:
        try:
            mqtt_client.listen()
            logging.info("Exiting")
        except BaseException as err:
            logging.exception(f"Unexpected exception, {type(err)} when connecting to mqtt server")
            raise
        finally:
            mqtt_client.client.disconnect()


if __name__ == '__main__':
    run_subscriber()
