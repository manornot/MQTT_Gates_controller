from Relay import Relay
from time import sleep


class Door():
    def __init__(self, actuator_pin, numbering, activeState, openTime=10):
        self.pin = actuator_pin
        self.numbering = numbering
        self.openTime = openTime
        assert type(activeState) is not str, "state cant be a string"
        assert type(activeState) is not list, "state cant be a list"
        self.activeState = Relay.HIGH if activeState else Relay.LOW
        self.relay = Relay(self.pin, self.numbering, self.activeState)

    def open(self):
        self.relay.setActive()
        sleep(self.openTime)
        self.relay.setInActive()
