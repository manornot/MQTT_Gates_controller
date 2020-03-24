import time
import numpy as np
import paho.mqtt.client as client
import sys

def main(msg):
    clnt = client.Client(client_id = 'user1')
    clnt.on_connect = on_connect
    clnt.on_message = on_message
    clnt.connect(host = broker,port = 1883)
    clnt.publish("gates/command",msg)    
    state_checker(clnt)

def on_connect(client, userdata, flags, rc):
    print("i'm in\n")
    client.subscribe(topic='gates/command', qos = 2)
    client.subscribe(topic='gates/state', qos = 2)

def on_message(client, userdata, message):
    print('message received')
    print(message.payload)

def state_checker(client):
    while True:
        client.loop(0.001)

broker = 'vtvm.edi.lv'
main(sys.argv[1])
