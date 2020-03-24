#!/usr/bin/env python3
import time
import numpy as np
import RPi.GPIO as gpio
import paho.mqtt.client as client
import paho.mqtt.publish
import threading

broker = 'vtvm.edi.lv'


#print('zap')

def main():
    global pin_state
    global opening_
    global stop_
    global open_
    global closing_
    global logic
    global err
    global close_
    clnt = client.Client(client_id = 'gatekeeper')
    clnt.on_connect = on_connect
    clnt.on_message = on_message
    clnt.connect(host = broker,port = 1883)
    state_checker(clnt)

def on_connect(client, userdata, flags, rc):
    print("i'm in\n")
    client.subscribe(topic='command', qos = 2)

def on_message(client, userdata, message):
#    print(client)
#    print('\n')
#    print(userdata)
#    print('\n')
#    print(message.topic,'\n',message.payload,'\n')

#    print('\n')
    if(message.payload == b'open' and not(open_) and not(opening_) and not(closing_)):
        gpio.output(11,1)
        #s.sendto(b'opening',addr)
        print("opening\n",open_,opening_,closing_,'\n')
        paho.mqtt.publish.single("response",'Roger Roger! Execute openning protocol!',hostname=broker)
        time.sleep(1)
        gpio.output(11,0)
    elif(message.payload == b'close' and not(close_) and not(closing_) and not(opening_)):
        gpio.output(11,1)
        #s.sendto(b'closing',addr)
        print("closing\n",close_,closing_,opening_,'\n')
        paho.mqtt.publish.single("response",'Roger Roger! Execute closing protocol!',hostname=broker)
        time.sleep(1)
        gpio.output(11,0)
    elif(message.payload == b'stop' and not(open_) and not(close_)):
        gpio.output(11,1)
        #s.sendto(b'stoped',addr)
        print("exterminate\n",open_,close_,'\n')
        paho.mqtt.publish.single("response",'Roger Roger! Execute extermination  protocol!',hostname=broker)
        time.sleep(1)       
        gpio.output(11,0)    
    elif(message.payload == b'status'):
        paho.mqtt.publish.single('state','Roger Roger',hostname=broker)
        





def state_checker(client):

    global close_
    global pin_state_
    global opening_
    global stop_
    global open_
    global closing_
    global logic
    global err
    global pin_state
    #0 - k3 - M1 - opening  
    #1 - k5 - M1 - closing 
    #2 - k6 - M2 - opening 
    #3 - k8 - M2 - closing 
    #4 - l6 - Limit switch open 
    #5 - l7 - Limit switch close
    print('woop')
    time.sleep(1)
    logic_prev = np.empty([])
    pin_state_prev = np.empty([])
    while True:
        close_ = np.array(not(pin_state[5]) and not(pin_state[0]) and not(pin_state[2])).astype(np.bool_)
        opening_ = np.array(pin_state[0] and pin_state[2]).astype(np.bool_)
        stop_ = np.array(pin_state[4] and pin_state[5] and not(pin_state[0] or pin_state[1] or pin_state[2] or pin_state[3])).astype(np.bool_)
        open_ = np.array(not(pin_state[4]) and not(pin_state[1]) and not(pin_state[3])).astype(np.bool_)
        closing_ = np.array(pin_state[1] and pin_state[3]).astype(np.bool_)
        #err = close_ + opening_ + stop_ + open_ + closing_
        pin_state_ = np.roll(pin_state_,1,axis=1)
        pin_state_[:,0] = read_pin()
        pin_state = np.round(pin_state_.mean(axis=1)).astype(np.bool_)
        #print(pin_state,close_,opening_,stop_,open_,closing_)
        logic = close_ | opening_<<1 | stop_<<2 | open_<<3 | closing_<<4
        client.loop(.1)
        if(np.array_equal(logic,logic_prev)):
            pass
        else:
            client.publish("state",str(logic))
            logic_prev = logic.copy()
        if(np.array_equal(pin_state,pin_state_prev)):
            pass
        else:
            client.publish("pin state",str(pin_state))
            pin_state_prev = pin_state.copy()

def read_pin():
    return [not(gpio.input(26)),not(gpio.input(19)),not(gpio.input(13)),not(gpio.input(6)),1,1,gpio.input(5)]

gpio.setmode(gpio.BCM)
gpio.setup(26,gpio.IN)
gpio.setup(19,gpio.IN)
gpio.setup(13,gpio.IN)
gpio.setup(6,gpio.IN)
gpio.setup(5,gpio.IN)
gpio.setup(11,gpio.OUT)
gpio.output(11,0)
closing_ = False
err = False
logic = False
open_ = False
stop_ = False
opening_ = False
close_ = True
pin_state_ = np.zeros((7,20))
pin_state = np.zeros(7)

#clnt = client.Client(client_id = 'gatekeeper')
#clnt.on_connect = on_connect
#clnt.on_message = on_message
#clnt.connect(host = broker,port = 1883)

main()

try:
    while 1:
        time.sleep(.1)

except KeyboardInterrupt:
    print('exterminate')
    print('the dead are useless')
