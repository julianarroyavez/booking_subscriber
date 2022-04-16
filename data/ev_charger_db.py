from datetime import datetime
from peewee import Model, SqliteDatabase, IntegerField, DateTimeField, TextField

db = SqliteDatabase(None)


def get_current_iso_utc_time():
    return datetime.utcnow().isoformat()


def current_epoch_time():
    dt = datetime.utcnow()
    epoch = datetime.utcfromtimestamp(0)
    delta = dt - epoch
    print(delta.total_seconds())
    return int(delta.total_seconds())


def iso_time_to_epoch(iso_time):
    utc_dt = datetime.strptime(iso_time, '%Y-%m-%dT%H:%M:%SZ')
    timestamp = (utc_dt - datetime(1970, 1, 1)).total_seconds()
    return timestamp


class BaseModel(Model):
    class Meta:
        database = db


class Otps(BaseModel):
    id = IntegerField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    connector_id = IntegerField()
    value = TextField()
    charger_point_id = IntegerField()
    status = TextField()
    expiration_date = IntegerField()
    booking_id = TextField()


class EvChargerDb:
    """access ev_charger database"""

    def __init__(self, db_path):
        db.init(db_path)

    @staticmethod
    def get_otp_by_value(otp_value):
        otp_found = Otps.select(Otps).where(Otps.value == otp_value)
        if len(otp_found) == 0:
            return None
        return otp_found[0]

    @staticmethod
    def get_otp_by_booking_id(booking_id):
        otp_found = Otps.select(Otps).where(Otps.booking_id == booking_id)
        if len(otp_found) == 0:
            return None
        return otp_found[0]

    def update_otp_status(self, booking_id, status):
        otp = self.get_otp_by_booking_id(booking_id)
        if otp is None:
            return None
        otp.status = status
        otp.save()
        return otp

    @staticmethod
    def insert_otp(otp):
        otp.save()
        return otp

    @staticmethod
    def update_otp(otp):
        otp.save()
        return otp
