#!/usr/bin/env python3
import time
import sys
import numpy as np
import RPi.GPIO as gpio
import paho.mqtt.client as client
import paho.mqtt.publish
import threading
import csv
fields = ['M00','MO1','M10','M11','time']
from fsm import gates_FSM
from filt_func import *
from queue import Queue
from smooth import *
broker = 
gates = gates_FSM()
available_commands = [b'open',b'stop',b'close']

def open_command(gate):
    #print('Roger Roger! Execute openning protocol!')
    #time.sleep(1)
    print(gate.state)
    if gate.state == 'close' or gate.state == 'stop':
        print('push me!')
        button_press()
def close_command(gate):    
    if gate.state == 'open':
           button_press()
    elif gate.state == 'stop':
        print(gate.prev_state)
        if gate.prev_state == 'opening':
            button_press()
        elif gate.prev_state == 'closing':
            button_press()
            time.sleep(3)
            button_press()
            time.sleep(3)
            button_press()
            time.sleep(3)
                  

def stop_command(gate):
    button_press()
   		
def button_press():
    #pass
    print('open this fucking doors')
    gpio.output(11,1)
    time.sleep(1)
    gpio.output(11,0)


def main(gates):
    client_data = {'gates':gates}
    clnt = client.Client(client_id = 'gatekeeper',userdata = client_data)
    clnt.on_connect = on_connect
    clnt.on_message = on_message 
    clnt.connect(host = broker,port = 1883)
    clnt.loop_start()
    state_checker(clnt,gates)


def on_connect(client, userdata, flags, rc):
    print("i'm in\n")
    sys.stdout.flush()
    client.disconnect_flag = False
    client.subscribe(topic='gates/command')

def on_message(client, userdata, message):
    print('message received=',message.payload,time.time()) 
    #print(userdata.get('gates').state)
    sys.stdout.flush()
    if(any(cmd == message.payload for cmd in available_commands)):
        print('its true')
        servetor_ai(userdata.get('gates'),message.payload)
        
def state_checker(clnt,gates):

    #0 - k3 - M1 - opening  
    #1 - k5 - M1 - closing 
    #2 - k6 - M2 - opening 
    #3 - k8 - M2 - closing 
    #4 - l6 - Limit switch open 
    #5 - l7 - Limit switch close
    print('woop')
    #time.sleep(1)
    state_fun = gates.unknown_state(read_pin())
    state = ''
    prev_state = ''
    pins = np.zeros([6])
    prev_pins = np.empty_like(pins)
    reads_counter = 0
    win_len = 100
    round_dig = 1
    win = 'hanning'
    pin_states = np.empty([0])
    while True:
        if reads_counter>win_len:
            pins,pin_states = filter_pins(pin_states,win,win_len,round_dig)
            state_fun = state_fun(np.rint(pins))
            state = gates.state
            #print(gates.state,gates.prev_state)
            #    with open('pin_log.csv','a') as f:
            #        writer = csv.writer(f)
            #        writer.writerow([read_pin()[0:4],time.time()])
            if(state == prev_state):
                pass
            else:
                clnt.publish("gates/state",str(state))
                prev_state = state
                sys.stdout.flush()
            time.sleep(0.1)
                    #print('boop')
        else:
            pin_states = np.append(pin_states,read_pin()[3])
            reads_counter+=1



def read_pin():
    return np.array([1 - gpio.input(26), 1 - gpio.input(19), 1 - gpio.input(13), 1 - gpio.input(6),1,1])#,gpio.input(5)]

def filter_pins(pin_states,win,win_len,dig):
    pins = read_pin()
    pin_states = np.roll(pin_states,-1)
    pin_states[-1] = read_pin()[3]
    motion_dir = np.round(smooth(pin_states,win_len,win),dig)
    motion_dir = np.array([np.mean(motion_dir)])
    #print(motion_dir)
    motion_dir[motion_dir>0.80] = 1
    motion_dir[motion_dir<0.50] = 2
    motion_dir[motion_dir<0.75] = -1
    motion_dir[motion_dir>1] = 0
    motion_dir = np.round(motion_dir,0)
    if int(motion_dir[0]) == 1:
        pins[0:4] = [1,0,1,0]
    elif int(motion_dir[0]) == -1:
        pins[0:4] = [0,1,0,1]
    else:
        pins[0:4] = 0
    return pins,pin_states
def nsc():
    print('i have no idea what do you want from me')

def servetor_ai(gate,msg):
    #new_command = 0
    print('servetor is online')
    print('command received')
    servetor.get(msg,nsc)(gate) 
    time.sleep(0.1)
	
gpio.setmode(gpio.BCM)
gpio.setup(26,gpio.IN)
gpio.setup(19,gpio.IN)
gpio.setup(13,gpio.IN)
gpio.setup(6,gpio.IN)
#gpio.setup(5,gpio.IN)
gpio.setup(11,gpio.OUT)
gpio.output(11,0)

protocol = [open_command,close_command,stop_command]
servetor = {
        b'open':protocol[0],
#        b'close':protocol[1],
#        b'stop':protocol[2]
}

#clnt = client.Client(client_id = 'gatekeeper')
#clnt.on_connect = on_connect
#clnt.on_message = on_message
#clnt.connect(host = broker,port = 1883)
main(gates)
try:
    while True:
        time.sleep(.1)
        sys.stdout.flush()

except KeyboardInterrupt:
    print('exterminate')
    print('the dead are useless')
