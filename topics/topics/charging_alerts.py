import json
import logging
from types import SimpleNamespace
from topics.topic_base import TopicBase

logging.basicConfig(level=logging.INFO)

class ChargingAlertsTopic(TopicBase):
    def do_action(self, msg, db_client, config):
        booking = json.loads(msg.payload, object_hook=lambda d: SimpleNamespace(**d))
        logging.info(f'otp id {booking.resource.bookingId} inserted to db, status {booking.resource.status}')
        db_client.update_otp_status(booking.resource.bookingId,booking.resource.status)   

