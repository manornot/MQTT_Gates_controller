from edi_doors import Doors
import binascii
import sys


DEBUG = False


def init(door):
    door.room = 319
    door.floor = 3
    door.building = 'B'
    door.host = ''  # '192.168.0.100'
    door.port = 1883
    door.command = 'command'
    door.status = 'status'

    door.mqtt_client.user_data_set(door)
    door.mqtt_client.on_connect = on_connect
    door.mqtt_client.on_message = on_message
    door.init()


door = Doors()
init(door)
if DEBUG:
    print(door)
door.mqtt_client.loop_start()
