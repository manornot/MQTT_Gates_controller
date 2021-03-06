import paho.mqtt.client as client
import paho.mqtt.publish
import logging
logger = logging.getLogger('MQTT')


class MQTT_Client:

    def dummyHandler(self):
        assert False, "you need to implement handler by your self"

    def __init__(self, room, floor,
                 building, host, port,
                 command_topic, status_topic, handler=dummyHandler):
        self.room = room
        self.floor = floor
        self.building = building
        self.host = host
        self.port = port
        self.__command = command_topic
        self.__status = status_topic
        self.mqtt_client = client.Client(
            client_id=f'{self.room}{self.building}')
        if handler is not self.dummyHandler:
            self.mqtt_client.message_callback_add(self.command_topic, handler)
            logger.debug(f'handler is {handler}')
        else:
            logger.debug(f'handler is {handler}')
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        logger.debug(f'{self}')

    def connect(self):
        self.mqtt_client.connect(host=self.host, port=self.port)
        self.mqtt_client.loop_start()
        logger.debug(f'connecting to  {self.host}')

    def on_connect(self, client, userdata, flags, rc):
        logger.debug(f'entered on_connect')
        client.subscribe(self.command_topic)
        logger.debug(f'subscribed to {self.command_topic}')

    def on_disconnect(self, client, userdata, rc):
        logger.critical(f'AHTUNG! no connection')

    def request_open(self, tag):
        self.user = tag
        logger.debug(f'publish to edi/user/{str(tag)}/{self.request_topic}')
        self.mqtt_client.publish(self.request_topic, str('open'))

    def topicBody(self):
        return f'{self.building}/{self.floor}/{self.room}'

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, uuid):
        self.__user = uuid

    @property
    def command_topic(self):
        self.__command_topic = f'edi/{self.topicBody()}/{self.__command}'
        return self.__command_topic

    @property
    def handler(self):
        pass

    @handler.setter
    def handler(self, handler):
        self.mqtt_client.message_callback_add(self.command_topic, handler)
        logger.debug(f'handler is set to{handler}')

    @property
    def status_topic(self):
        self.__status_topic = f'edi/{self.topicBody()}/{self.__status}'

    @property
    def request_topic(self):
        self.__request_topic = f'edi/user/{self.user}/{self.topicBody()}'
        return self.__request_topic

    def __str__(self):
        return f'room {self.room} Building {self.building} floor {self.floor}\nhost = {self.host} port = {self.port}\ncommand topic = {self.command_topic}\nstatus topic = {self.status_topic}'
