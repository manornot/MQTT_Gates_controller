import time
from Rfid import RFID_Reader
import Relay
from Door import Door
from MQTT_Client import MQTT_Client
import logging

logging.basicConfig(level=logging.DEBUG)


class Room():
    def __init__(self, room, floor,
                 building, host, port,
                 command_topic, status_topic,
                 actuator_pin, pin_numbering='BCM',
                 activeState=1,
                 CS=8, MOSI=10, MISO=9, SCLK=11):
        self.room = room
        self.floor = floor
        self.building = building
        self.id = str(self.room)+str(building)
        self.mqtt = MQTT_Client(room, floor,
                                building, host, port,
                                command_topic, status_topic)
        self.door = Door(actuator_pin=actuator_pin,
                         numbering=pin_numbering,
                         activeState=activeState)
        self.rfid = RFID_Reader(CS=CS,
                                MOSI=MOSI,
                                MISO=MISO,
                                SCLK=SCLK)
        self.available_commands = {b'open': self.door.open}

    def routine_start(self):
        self.mqtt.handler = self.door.open
        self.rfid.handler = self.mqtt.request_open
        while True:
            uid = self.rfid.readUID()
            if uid is not None:
                logging.debug(f'uid is {uid}')
                self.rfid.handler(uid)
                uid_old, uid_new = uid, uid
                while uid_old == uid_new:
                    uid_new = self.rfid.readUID()
                    if uid is None:
                        break
                    time.sleep(0.5)
            else:
                time.sleep(0.5)
