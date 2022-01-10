import json
import logging
from types import SimpleNamespace
from data.ev_charger_db import Otps, iso_time_to_epoch
from topics.topic_base import TopicBase


class BookingsTopic(TopicBase):
    def do_action(self, msg, db_client, config):
        logging.info(msg.payload)
        booking = json.loads(msg.payload, object_hook=lambda d: SimpleNamespace(**d))
        # filtered_bookings = [booking for booking in bookings
        #                      if booking.resource.station.id == config.station_id]

        # for booking in filtered_bookings:
        otp_from_db = db_client.get_otp_by_value(booking.resource.serviceOtp)
        if otp_from_db is None:
            otp = Otps()
            otp.start_time = booking.resource.serviceDate + \
                "T" + booking.resource.slot.startTime + "Z"
            otp.end_time = booking.resource.serviceDate + \
                "T" + booking.resource.slot.endTime + "Z"
            otp.value = booking.resource.serviceOtp
            otp.status = booking.resource.status
            otp.booking_id = booking.resource.bookingId
            otp.connector_id = 1  # todo
            otp.charger_point_id = config.charger_point_id
            otp.expiration_date = iso_time_to_epoch(otp.end_time)
            db_client.insert_otp(otp)
        else:
            otp_from_db.status = booking.resource.status
            otp_from_db.start_time = booking.resource.serviceDate + \
                "T" + booking.resource.slot.startTime + "Z"
            otp_from_db.end_time = booking.resource.serviceDate + \
                "T" + booking.resource.slot.endTime + "Z"
            db_client.insert_otp(otp_from_db)
