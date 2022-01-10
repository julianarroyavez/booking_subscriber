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

    def __init__(self, mqtt_config, booking_subscriber_configuration, ev_db):
        super().__init__(mqtt_config)
        self.client.on_message = self.on_message
        self.client_id = mqtt_config.id
        self._db_client = ev_db
        self.config = booking_subscriber_configuration
