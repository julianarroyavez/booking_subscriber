import json
from types import SimpleNamespace
from topics.topic_base import TopicBase


class ChargingAlertsTopic(TopicBase):
    def do_action(self, msg, db_client, config):
        booking = json.loads(msg.payload, object_hook=lambda d: SimpleNamespace(**d))
        db_client.update_otp_status(booking.resource.bookingId, booking.resource.status)
