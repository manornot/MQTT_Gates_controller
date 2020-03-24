import time
import numpy as np
import RPi.GPIO as gpio
import paho.mqtt.client as client
import paho.mqtt.publish
import threading
import sys
from queue import Queue
broker = 
from garage_fsm import garage_gates_FSM
available_commands = [b'open',b'stop',b'close']
debug_pins_state = '11111'

CL,OP,K,_open,G,_close,T,_stop = 8,10,12,16,18,22,24,26

gpio.setmode(gpio.BOARD)

def read_pins():
    return str(gpio.input(CL)) + str(gpio.input(OP)) + str(gpio.input(K)) + str(gpio.input(G)) + str(gpio.input(T))

        
def state_checker(client,gates):
    print('woop')
    state_fun = gates.unknown_state(read_pins())
    state = ''
    prev_state = ''
    _counter = 0
    while True:
        pins = read_pins()
        state_fun = state_fun(pins)
        state = gates.state
        if(state == prev_state):
            _counter+=1
            #print(_counter)
            if(_counter%1000==0):
                client.publish("garage/check","im ok too " + str(_counter))
                time.sleep(0.1)
            pass
        else:
            client.publish("garage/state",str(state))
            print(state,pins)
            prev_state = state
            sys.stdout.flush()
        client.loop(0.01)


def main(gates,thread_msg):
    while(True):
        clnt = client.Client(client_id = 'garagekeeper')
        clnt.on_connect = on_connect
        clnt.on_message = on_message
        clnt.connect(host = broker,port = 1883)
        state_checker(clnt,gates)

def on_connect(client, userdata, flags, rc):
    print("i'm in\n")
    client.subscribe(topic="garage/command", qos = 2)
    sys.stdout.flush()

def on_message(client, userdata, message):
    print('message received = ',message.payload,time.time())
    sys.stdout.flush()
    if(any(cmd == message.payload for cmd in available_commands)):
        q.put(message.payload)

def nop():
    print('i have no idea what do you want from me')
    sys.stdout.flush()
    pass

def servetor_ai(thread_msg):
    print('servetor is online')
    sys.stdout.flush()
    counter = 0
    while True:
        if not thread_msg.empty():
            print('command received')
            mqtt_command = thread_msg.get()
            print(mqtt_command)
            servetor.get(mqtt_command,nop)()
        counter +=1
        if(counter % 1000 == 0 ):
            #print('im ok ' + str(time.time()))
            time.sleep(0.1)
            


def init_pins(CL,OP,K,G,T,_open,_close,_stop):
    
    gpio.setup(CL,gpio.IN)
    gpio.setup(OP,gpio.IN)
    gpio.setup(K,gpio.IN)
    gpio.setup(G,gpio.IN)
    gpio.setup(T,gpio.IN)
    gpio.setup(_open,gpio.OUT)
    gpio.output(_open,0)
    gpio.setup(_close,gpio.OUT)
    gpio.output(_close,0)
    gpio.setup(_stop,gpio.OUT)
    gpio.output(_stop,0)

def open_command():
    paho.mqtt.publish.single("garage/response",'Roger Roger! Execute openning protocol!',hostname=broker)
    time.sleep(1)
    if gates.state == 'close' or gates.state == 'stop':
        press['open']()
    elif gates.state == 'closing':
        press['stop']()
        time.sleep(1)
        press['open']()

def close_command():    
    if gates.state == 'open' or gates.state == 'stop':
        press['close']()
    elif gates.state == 'opening':
        press['stop']()
        time.sleep(1)
        press['close']()
                  
def stop_command():
    press['stop']()

def press_open(pin=_open):
    gpio.output(_open,1)
    time.sleep(1)
    gpio.output(_open,0)

def press_stop(pin=_stop):
    gpio.output(_stop,1)
    time.sleep(1)
    gpio.output(_stop,0)

def press_close(pin=_close):
    gpio.output(_close,1)
    time.sleep(1)
    gpio.output(_close,0)



press = {'open':press_open,'close':press_close,'stop':press_stop}
servetor = {
        b'open':open_command,
        b'close':close_command,
        b'stop':stop_command,
        }
init_pins(CL,OP,K,G,T,_open,_close,_stop)
gates = garage_gates_FSM()
state_fun = gates.unknown_state(read_pins())
pins = read_pins()
state_fun = state_fun(pins)
state = gates.state
print(state)
q = Queue()
threading.Thread(target=servetor_ai, args =(q,)).start()
threading.Thread(target=main, args = (gates,q,)).start()

try:
    while 1:
        time.sleep(.1)
        sys.stdout.flush()
except KeyboardInterrupt:
    print('exterminate')
    print('the dead are useless')
