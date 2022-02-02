import paho.mqtt.client as mqtt


class MQTTClient(object):
    """base mqtt hygge client - server connection"""

    def __init__(self, config):
        self.client = mqtt.Client(client_id=config.id, clean_session=False)
        self.errors = None
        self.config = config
        self.client_id = config.id
        self.client.on_connect = self._on_connect
        self.client.on_subscribe = self._on_subscribe
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        self.client.on_disconnect = self._on_disconnect

        self.client.username_pw_set(config.username, config.password)
        self.client.connect(config.host, config.port)
        for topic in config.topics:
            self.client.subscribe(topic.topic, topic.qos)

    def _on_connect(self, _, __, flags, rc):
        print(
            f"Connected {self.client_id}, result code: {str(rc)} {str(flags)}")

    def _on_subscribe(self, _, __, mid, granted_qos):
        print(
            f"Subscribed {self.client_id}, mid: {mid}, granted qos: {granted_qos}")
        print(f"Listening for {self.client_id} messages...")

    def _on_disconnect(self, _, __, rc):
        print(f"Disconnected {self.client_id}, result code: {str(rc)}")

    def _on_message(self, _, __, msg):
        print(
            f"Client: {self.client_id} Topic: {msg.topic}, Mid: {msg.mid}, Payload: {msg.payload.decode('utf-8')}")

    def _on_publish(self, _, __, mid):
        print(f"Published by {self.client_id}, mid: {mid}")

    def listen(self):
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            print(
                f"Received KeyboardInterrupt, disconnecting {self.config.mqtt.id}")
            self.client.disconnect()
