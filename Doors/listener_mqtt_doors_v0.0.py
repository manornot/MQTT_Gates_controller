# init room
# init mqtt
# connect to mqtt
# init rfid
# rfid reading
#   if read_rfid():
#       send_request()

from edi_doors import Doors
import binascii
import sys
import Adafruit_PN532 as PN532
DEBUG = False


def on_connect(client, userdata, flags, rc):
    if DEBUG:
        print(userdata)
    if rc == 0:
        if DEBUG:
            print("connected OK Returned code=", rc)
        client.subscribe(userdata.command_topic)
    else:
        if DEBUG:
            print("Bad connection Returned code=", rc)


def on_message(client, userdata, message):
    if DEBUG:
        print(message.payload in userdata.available_commands)
    if message.payload in userdata.available_commands:
        userdata.available_commands.get(message.payload)()


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
    #door.mqtt_client.username_pw_set(username='jura', password='qweasdzxc')
    door.init()


door = Doors()
init(door)
if DEBUG:
    print(door)
door.mqtt_client.loop_start()


# Setup how the PN532 is connected to the Raspbery Pi/BeagleBone Black.
# It is recommended to use a software SPI connection with 4 digital GPIO pins.

# Configuration for a Raspberry Pi:
CS = 8
MOSI = 10
MISO = 9
SCLK = 11


pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
ic, ver, rev, support = pn532.get_firmware_version()
if DEBUG:
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
pn532.SAM_configuration()
if DEBUG:
    print('Waiting for MiFare card...')
while True:
    uid = pn532.read_passive_target()
    if uid is None:
        continue
    if DEBUG:
        print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
        if DEBUG:
            print('Failed to authenticate block 4!')
        continue
    data = pn532.mifare_classic_read_block(4)
    if data is None:
        if DEBUG:
            print('Failed to read block 4!')
        continue
    if DEBUG:
        print('Read block 4: 0x{0}'.format(binascii.hexlify(data[:4])))
    uuid = str('{0}'.format(binascii.hexlify(uid)))[2:-1]
    door.request_open(uuid)
    if DEBUG:
        print(f'edi/user/{uuid}/{door.request_topic}')
    uid_old, uid_new = uid, uid
    while uid_old == uid_new:
        uid_new = pn532.read_passive_target()
        if uid is None:
            break
        pass
