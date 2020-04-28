import paho.mqtt.client as clnt
import paho.mqtt.publish
from edi_doors import Doors
import os
from csv import reader
DEBUG = False


def on_connect(client, userdata, flags, rc):
    if DEBUG:
        print(f'userdata = {userdata}')
    for user in userdata:
        if DEBUG:
            print(f'user = {user}')
        for door in user.__rooms:
            if DEBUG:
                print(f'door = {door}, uuid = {user.user}')
            user.room = door
            user.__user = user.user
            tpk = user.request_topic
            if DEBUG:
                print(tpk)
            client.subscribe(tpk)


def on_message(client, userdata, message):
    if DEBUG:
        print(f'topic = {message.topic} payload = {message.payload}')
    door = Doors()
    *_, building, floor, room = message.topic.split('/')
    if DEBUG:
        print(f'{building}, {floor}, {room}')

    door.building = building
    door.floor = floor
    door.room = room
    door.command = 'command'
    if DEBUG:
        print(f'publishing to {door.command_topic}')
    client.publish(door.command_topic, str('open'))


read_data = []
file = "\\access.csv"
path = os.getcwd()+file
path = path.replace('\\', '/')
with open(path) as f:
    for row in reader(f):
        read_data.append(row)
to_subscribe = []
for line in read_data:
    if DEBUG:
        print(line)
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
