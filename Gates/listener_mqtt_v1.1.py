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

def open_command():
    paho.mqtt.publish.single("response",'Roger Roger! Execute openning protocol!',hostname=broker)
    time.sleep(1)
    if gates.state == 'close' or gates.state == 'stop':
        button_press()
def close_command():    
    if gates.state == 'open':
           button_press()
    elif gates.state == 'stop':
        print(gates.prev_state)
        if gates.prev_state == 'opening':
            button_press()
        elif gates.prev_state == 'closing':
            button_press()
            time.sleep(3)
            button_press()
            time.sleep(3)
            button_press()
            time.sleep(3)
                  

def stop_command():
    button_press()
   		
def button_press():
    #pass
    gpio.output(11,1)
    time.sleep(1)
    gpio.output(11,0)


def main(gates,thread_msg):
    while(True):
        clnt = client.Client(client_id = 'gatekeeper')
        clnt.on_connect = on_connect
        clnt.on_message = on_message
        clnt.on_disconnect = on_disconnect
        clnt.connect(host = broker,port = 1883)
        state_checker(clnt,gates)


def on_connect(client, userdata, flags, rc):
    print("i'm in\n")
    sys.stdout.flush()
    client.disconnect_flag = False
    client.subscribe(topic='gates/command', qos = 2)

def on_message(client, userdata, message):
    print('message received=',message.payload,time.time()) 
    sys.stdout.flush()
    if(any(cmd == message.payload for cmd in available_commands)):
        q.put(message.payload)
def on_disconnect(client, user, flags, rc):
    sys.stdout.flush()
    logging.info("disconnecting reason " + str(rc))
    client.disconnect_flag = True
       
        
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
            clnt.loop(0.01)
                    #time.sleep(0.5)
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

def servetor_ai(thread_msg):
    new_command = 0
    print('servetor is online')
    while True:
        if not thread_msg.empty():
            print('command received')
            mqtt_command = thread_msg.get()
            servetor.get(mqtt_command,nsc)()
	
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
}

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
