import paho.mqtt.client as client
import paho.mqtt.publish
import logging
import os

logger = logging.getLogger('requester')


class Doors():
    def __init__(self, room='', floor='',
                 building='', host='', port='',
                 command_topic='', status_topic=''):
        self.room = room
        self.floor = floor
        self.building = building
        self.host = host
        self.port = port
        self.__command_topic = ''
        self.__status_topic = ''
        self.__request_topic = ''
        self.userdata = ''
        self.__user = ''
        self.command = ''
        self.status = ''
        self.id = str(self.room)+str(building)
        self.mqtt_client = client.Client()
        self.available_commands = {b'open': self.open}

    def request_open(self, tag):
        logger.debug(f'publish to edi/user/{str(tag)}/{self.request_topic}')
        self.__user = tag
        self.mqtt_client.publish(self.request_topic, str('open'))

    def open(self):
        logger.debug(f'AAAAAAAAAAAAAAAAA i am fcking done')
        pass

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, uuid):
        self.__user = uuid

    @property
    def command_topic(self):
        self.__command_topic = f'edi/{self.building}/{self.floor}/{self.room}/{self.command}'
        return self.__command_topic

    @property
    def status_topic(self):
        self.__status_topic = f'edi/{self.building}/{self.floor}/{self.room}/{self.status}'

    @property
    def request_topic(self):
        self.__request_topic = f'edi/user/{self.__user}/{self.building}/{self.floor}/{self.room}'
        return self.__request_topic

    def params(self):
        return {'room': self.room, 'building': self.building, 'floor': self.floor, 'host': self.host, 'port': self.port, 'command topic': self.command_topic, 'status topic': self.status_topic}

    def __str__(self):
        return f'room {self.room} Building {self.building} floor {self.floor}\nhost = {self.host} port = {self.port}\ncommand topic = {self.command_topic}\nstatus topic = {self.status_topic}'

    def init(self):
        self.mqtt_client._client_id = f'{self.room}{self.building}'
        self.mqtt_client.connect(host=self.host, port=self.port)
