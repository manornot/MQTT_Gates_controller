import logging
import time
import paho.mqtt.client as clnt
import paho.mqtt.publish
from edi_doors import Doors
import os
from csv import reader
DEBUG = False
LOG = False
path_to_log = 'doors.log'


def on_connect(client, userdata, flags, rc):
    logger.debug(f'userdata = {userdata}')
    for user in userdata:
        logger.debug(f'user = {user}')
        for door in user.__rooms:
            logger.debug(f'door = {door}, uuid = {user.user}')
            user.room = door
            user.__user = user.user
            tpk = user.request_topic
            logger.debug(tpk)
            client.subscribe(tpk)


def on_message(client, userdata, message):
    logger.debug(f'topic = {message.topic} payload = {message.payload}')
    door = Doors()
    *_, building, floor, room = message.topic.split('/')
    logger.debug(f'{building}, {floor}, {room}')

    door.building = building
    door.floor = floor
    door.room = room
    door.command = 'command'
    logger.debug(f'publishing to {door.command_topic}')
    logger.info(f'authorised access request to {door} by {message.topic}')
    client.publish(door.command_topic, str('open'))


if DEBUG:
    logging.basicConfig(filename=path_to_log, level=logging.DEBUG)
    logging.debug("DEBUG IS EBABLED")
elif LOG:
    logging.basicConfig(filename=path_to_log, level=logging.INFO)
logger = logging.getLogger('server')
read_data = []
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
rel_path = "access.csv"
path = os.path.join(script_dir, rel_path)
logger.debug(f'local path {path}')
with open(path) as f:
    for row in reader(f):
        read_data.append(row)
to_subscribe = []
for line in read_data:
    logger.debug(f'{line}')
    user, building, floor, *rooms = line
    door = Doors()
    door.user = user
    door.building = building
    door.floor = floor
    door.__rooms = rooms
    to_subscribe.append(door)

server = clnt.Client(client_id='server')
server.on_connect = on_connect
server.on_message = on_message
server.user_data_set(to_subscribe)
server.connect(host='localhost', port=1883)

server.loop_forever()
