import logging
import sys
from enum import Enum
from configobj import ConfigObj

logger = logging.getLogger('HYGGE BOOKING SUBSCRIBER')


class ErrorLevel(Enum):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class BookingSubscriberConfiguration:
    def __init__(self, file_path):
        self.config = ConfigObj(file_path)
        self.project_db_path = self.config["project_db_path"]
        self.station_id = self.config['booking_subscriber']["station_id"]
        self.charger_point_id = self.config['booking_subscriber']["charger_point_id"]
        self.mqtt = self.__get_mqtt_config()
        self.__config_log()

    def __booking_subscriber(self):
        data = self.config['booking_subscriber']
        temp_obj = self.ConfigObject()
        temp_obj.station_id = data["station_id"]
        temp_obj.charger_point_id = data["charger_point_id"]
        return temp_obj

    def __get_mqtt_config(self):
        data = self.config['mqtt']
        temp_obj = self.ConfigObject()
        temp_obj.username = data["username"]
        temp_obj.password = data["password"]
        temp_obj.id = data["id"]
        temp_obj.port = int(data["port"])
        temp_obj.host = data["host"]
        topics = self.config['booking_subscriber']["topics"]
        temp_obj.topics = []
        for t in topics:
            topic = self.ConfigObject()
            topic.topic = t.split(' ')[0]
            topic.qos = int(t.split(' ')[1])
            temp_obj.topics.append(topic)
        return temp_obj

    def __config_log(self):
        log_format = '%(asctime)s | %(levelname)s | %(message)s'
        time_format = '%m-%d-%Y %H:%M:%S'
        log_file = self.config["logging_file"]
        log_level = self.config["logging_level"]
        level = ErrorLevel[log_level]

        logging.basicConfig(
            filename=log_file,
            format=log_format,
            level=level.value,
            datefmt=time_format)

        stdout_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(log_format, time_format)
        stdout_handler.setFormatter(formatter)
        stdout_handler.setLevel(level.value)

        global logger
        logger = logging.getLogger()
        logger.addHandler(stdout_handler)
        logger.info('Set log file to: ' + log_file)

    class ConfigObject:
        pass
