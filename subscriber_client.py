from configuration import BookingSubscriberConfiguration
from data.ev_charger_db import EvChargerDb
from mqtt.mqtt_base_client import MQTTClient
import logging
from topics.topics_factory import TopicFactory


class BookingSubscriberClient(MQTTClient):
    def on_message(self, _, __, msg):
        try:
            topic = TopicFactory.get_topic_subscriber(msg.topic)
            topic.do_action(msg, self._db_client, self.config)

        except BaseException as err:
            print(
                f"Unexpected {err}, {type(err)} when getting booking messages")
            logging.error(str(err))

    def __init__(self, config: BookingSubscriberConfiguration, ev_db: EvChargerDb):
        super().__init__(config.mqtt)
        self.client.on_message = self.on_message
        self.client_id = config.mqtt.id
        self._db_client = ev_db
        self.config = config
