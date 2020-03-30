import time
import numpy as np
import RPi.GPIO as gpio
import paho.mqtt.client as client
import paho.mqtt.publish
#import threading
import sys
from queue import Queue
broker = 
from garage_fsm import garage_gates_FSM
DEBUG = True
available_commands = [b'open',b'stop',b'close']
debug_pins_state = '11111'

CL,OP,K,_open,G,_close,T,_stop = 8,10,12,16,18,22,24,26

gpio.setmode(gpio.BOARD)

def read_pins():
    return str(gpio.input(CL)) + str(gpio.input(OP)) + str(gpio.input(K)) + str(gpio.input(G)) + str(gpio.input(T))

        
def state_checker(client,gates):
    if DEBUG: print('DEBUG','woop')
    state_fun = gates.unknown_state(read_pins())
    state = ''
    prev_state = ''
    _counter = 0
    while True:
        time.sleep(0.1)
        pins = read_pins()
        state_fun = state_fun(pins)
        state = gates.state
        if(state == prev_state):
            pass
        else:
            client.publish("garage/state",str(state))
            if DEBUG: 
                print('DEBUG',state,pins)
                sys.stdout.flush()
            prev_state = state


def main(gates):
    client_data = {'gates':gates}
    clnt = client.Client(client_id = 'garagekeeper',userdata = client_data)
    clnt.on_connect = on_connect
    clnt.on_message = on_message
    clnt.connect(host = broker,port = 1883)
    clnt.loop_start()
    state_checker(clnt,gates)

def on_connect(client, userdata, flags, rc):
    if DEBUG: print('DEBUG',"i'm in\n")
    client.subscribe(topic="garage/command", qos = 2)
    sys.stdout.flush()

def on_message(client, userdata, message):
    if DEBUG: print('DEBUG','message received = ',message.payload,time.time())
    sys.stdout.flush()
    if(any(cmd == message.payload for cmd in available_commands)):
        if DEBUG: print('its true')
        servetor_ai(userdata.get('gates'),message.payload)

def nop():
    if DEBUG: print('DEBUG','i have no idea what do you want from me')
    sys.stdout.flush()
    pass

def servetor_ai(gate,msg):
    #new_command = 0
    print('servetor is online')
    print('command received = ',msg)
    servetor.get(msg,nsc)(gate) 
    #time.sleep(0.1)
            


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

def open_command(gate):
    #paho.mqtt.publish.single("garage/response",'Roger Roger! Execute openning protocol!',hostname=broker)
    #time.sleep(1)
    if DEBUG: print('DEBUG','Open this fucking gates! motherfucker!')
    if gate.state == 'close' or gate.state == 'stop':
        press['open']()
    elif gate.state == 'closing':
        press['stop']()
        time.sleep(1)
        press['open']()

def close_command(gate):    
    if gate.state == 'open' or gate.state == 'stop':
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
if DEBUG: print('DEBUG',state)
main(gates)
try:
    while True:
        time.sleep(.1)
        sys.stdout.flush()
except KeyboardInterrupt:
    if DEBUG: print('DEBUG','exterminate')
    if DEBUG: print('DEBUG','the dead are useless')
    pass
