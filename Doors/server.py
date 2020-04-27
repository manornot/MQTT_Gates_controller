import paho.mqtt.client as clnt
import paho.mqtt.publish
from edi_doors import Doors
from csv import reader


def on_connect(client, userdata, flags, rc):
    for user in userdata:
        for door in user.__rooms:
            user.room = door
            client.subscribe(user.request_topic)


def on_message(client, userdata, message):
    door = Doors
    *_, building, floor, room = '/'.split(message.topic)
    door.building = building
    door.floor = floor
    door.room = room
    door.command = 'command'
    client.publish(door.command_topic, str('open'))


read_data = []
with open('D:/Dropbox/Ju\EDI/Autodrive/InfraStructure/GarageDoorController/mqtt_listener/Doors/access.csv') as f:
    for row in reader(f):
        read_data.append(row)
to_subscribe = []
for line in read_data:
    print(line)
    user, building, floor, *rooms = line
    door = Doors()
    door.user = user
    door.building = building
    door.floor = floor
    door.__rooms = rooms
    door.request_topic = ''
    to_subscribe.append(door)

server = clnt.Client(client_id='server')
server.user_data_set(to_subscribe)
server.connect(host='vtvm.edi.lv')

server.loop_forever()

# print(to_subscribe[0].request_topic)
