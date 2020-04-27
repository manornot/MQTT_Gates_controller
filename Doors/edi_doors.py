import paho.mqtt.client as client
import paho.mqtt.publish
import os


class Doors():
    def __init__(self, room=None, floor=None,
                 building=None, host=None, port=None,
                 command_topic=None, status_topic=None):
        self.room = room
        self.floor = floor
        self.building = building
        self.id = str(self.room)+str(building)
        self.__command_topic = f'edi/{building}/{floor}/{room}/{command_topic}'
        self.__status_topic = f'edi/{building}/{floor}/{room}/{status_topic}'
        self.userdata = {}
        self.host = host
        self.port = port
        self.mqtt_client = client.Client()
        self.available_commands = {b'open': self.open}

    def open(self):
        print('open the doors')

    @property
    def command_topic(self):
        return self.__command_topic

    @command_topic.setter
    def command_topic(self, topic):
        self.__command_topic = f'edi/{self.building}/{self.floor}/{self.room}/{topic}'

    @property
    def status_topic(self):
        return self.__status_topic

    @status_topic.setter
    def status_topic(self, topic):
        self.__status_topic = f'edi/{self.building}/{self.floor}/{self.room}/{topic}'

    def params(self):
        return {'room': self.room, 'building': self.building, 'floor': self.floor, 'host': self.host, 'port': self.port, 'command topic': self.command_topic, 'status topic': self.status_topic}

    def __str__(self):
        return f'room {self.room} Building {self.building} floor {self.floor}\nhost = {self.host} port = {self.port}\ncommand topic = {self.command_topic}\nstatus topic = {self.status_topic}'

    def init(self):
        self.mqtt_client._client_id = f'{self.room}{self.building}'
        self.mqtt_client.connect(host=self.host, port=self.port)

    # clnt.loop_start()


#door = Doors(319, 3, 'B', 'vtvm.edi.lv', 1883, 'command', 'status')
#door = Doors()
#door.room = 319
#door.floor = 3
#door.building = 'B'
#door.host = '192.168.0.100'
#door.port = 1883
#door.command_topic = 'command'
#door.status_topic = 'status'
# print(door)
