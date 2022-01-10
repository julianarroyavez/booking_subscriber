from topics.topics.bookings import BookingsTopic
from topics.topics.charging_alerts import ChargingAlertsTopic


class TopicFactory:
    @staticmethod
    def get_topic_subscriber(topic):
        if "charging-alert" in topic:
            t = ChargingAlertsTopic()
            return t
        if "booking" in topic:
            t = BookingsTopic()
            return t
