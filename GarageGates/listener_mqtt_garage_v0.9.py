#!/usr/bin/env python3
import time
import numpy as np
import RPi.GPIO as gpio
import paho.mqtt.client as client
import paho.mqtt.publish
import threading
import csv
fields = ['M00','MO1','M10','M11','time']
from fsm import gates_FSM
from filt_func import *
broker = 'vtvm.edi.lv'


#print('zap')

def main(gates):
    clnt = client.Client(client_id = 'gatekeeper')
    clnt.on_connect = on_connect
    clnt.on_message = on_message
    clnt.connect(host = broker,port = 1883)
    state_checker(clnt,gates)

def on_connect(client, userdata, flags, rc):
    print("i'm in\n")
    client.subscribe(topic='command', qos = 2)

def on_message(client, userdata, message):
    print(client)
    print(userdata)
    print(message.payload,gates.state)
    print(message.payload == b'open' and gates.state != 'open' and  gates.state != 'opening' and gates.state != 'closing')

#    print('\n')
    if message.payload == b'open' and gates.state != 'open' and gates.state != 'opening' and gates.state != 'closing':
        gpio.output(11,1)
        #s.sendto(b'opening',addr)
        print("opening")
        paho.mqtt.publish.single("response",'Roger Roger! Execute openning protocol!',hostname=broker)
        time.sleep(1)
        gpio.output(11,0)
    elif message.payload == b'close' and gates.state != 'close' and gates.state != 'opening' and gates.state != 'closing':
        gpio.output(11,1)
        paho.mqtt.publish.single("response",'Roger Roger! Execute closing protocol!',hostname=broker)
        time.sleep(1)
        gpio.output(11,0)
    elif message.payload == b'stop' and gates.state != 'close' and gates.state != 'open' and gates.state != 'stop':
        gpio.output(11,1)
        #s.sendto(b'stoped',addr)
        print("exterminate\n",open_,close_,'\n')
        paho.mqtt.publish.single("response",'Roger Roger! Execute extermination  protocol!',hostname=broker)
        time.sleep(1)       
        gpio.output(11,0)    
    elif(message.payload == b'status'):
       paho.mqtt.publish.single('state','Roger Roger',hostname=broker)
       paho.mqtt.publish.single('pins',str(read_pin()),hostname=broker)
        
def state_checker(client,gates):

    #0 - k3 - M1 - opening  
    #1 - k5 - M1 - closing 
    #2 - k6 - M2 - opening 
    #3 - k8 - M2 - closing 
    #4 - l6 - Limit switch open 
    #5 - l7 - Limit switch close
    print('woop')
    time.sleep(1)
    state_fun = gates.unknown_state(read_pin())
    state = ''
    prev_state = ''
    pins = np.zeros([6])
    prev_pins = np.empty_like(pins)
    params1 = [0.0001,0.5,0,0,1,0,0,0]
    params2 = [0.0001,0.5,0,0,1,0,0,0]
    params4 = [0.0001,0.5,0,0,1,0,0,0]
    params_mot = [0.0001,0.5,0,0,1,0,0,0]
    
    state_pos = 0
    state_neg = 0
    while True:
        pins = read_pin()
        M00 = pins[0]
        M01 = pins[1]
        M11 = pins[3]
        M00_filt,params1 = kalm_filt_iter(M00,params1)
        M01_filt,params2 = kalm_filt_iter(M01,params2)
        M11_filt,params4 = kalm_filt_iter(M11,params4)
        mot = 2*M00_filt - M01_filt - M11_filt
        mot_filt,params_mot = kalm_filt_iter(mot,params_mot)
        mot_pos,state_pos = hist_th(mot_filt,0.15,0.05,state_pos)
        mot_neg,state_neg = hist_th(-mot_filt,0.15,0.05,state_neg)
        mot = mot_pos-mot_neg
        if(mot == 1):
            pins[0:4] = 0,1,0,1
        elif(mot == -1):
            pins[0:4] = 1,0,1,0
        else:
            pins[0:4] = 0,0,0,0

        state_fun = state_fun(np.rint(pins))
        state = gates.state
    #    with open('pin_log.csv','a') as f:
    #        writer = csv.writer(f)
    #        writer.writerow([read_pin()[0:4],time.time()])
        client.loop(0.01)
        if(state == prev_state):
            pass
        else:
            client.publish("state",str(state))
            prev_state = state
        if str(pins) == str(prev_pins):
            pass
        else:
            #client.publish("pins",str(pins))
            print(str(pins))
            prev_pins = pins


def read_pin():
    return np.array([1 - gpio.input(26), 1 - gpio.input(19), 1 - gpio.input(13), 1 - gpio.input(6),1,1])#,gpio.input(5)]

gpio.setmode(gpio.BCM)
gpio.setup(26,gpio.IN)
gpio.setup(19,gpio.IN)
gpio.setup(13,gpio.IN)
gpio.setup(6,gpio.IN)
#gpio.setup(5,gpio.IN)
gpio.setup(11,gpio.OUT)
gpio.output(11,0)

#clnt = client.Client(client_id = 'gatekeeper')
#clnt.on_connect = on_connect
#clnt.on_message = on_message
#clnt.connect(host = broker,port = 1883)

gates = gates_FSM()
main(gates)

try:
    while 1:
        time.sleep(.1)

except KeyboardInterrupt:
    print('exterminate')
    print('the dead are useless')
