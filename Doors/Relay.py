#import RPi.GPIO as gpio

from raspberry_pc_debug import gpio


class Relay:
    HIGH = True
    LOW = False

    def __init__(self, pin, pin_numbering, activeState):
        self.__pin = pin
        self.__pin_numbering = pin_numbering
        self.activeState = activeState
        self.off = not self.activeState
        self.on = self.activeState
        self.states = [self.on, self.off]
        self.state = self.off
        gpio.setmode(pin_numbering)
        gpio.setup(self.__pin, gpio.OUT)

    def __setHigh(self):
        gpio.output(self.__pin, gpio.HIGH)

    def __setLow(self):
        gpio.output(self.__pin, gpio.LOW)

    def setActive(self):
        assert self.state in self.states, "initial state is not set"
        if self.state is self.off:
            if self.activeState is Relay.HIGH:
                self.__setHigh()
            else:
                self.__setLow()

    def setInActive(self):
        assert self.state in self.states, "initial state is not set"
        if self.state is self.on:
            if self.activeState is Relay.HIGH:
                self.__setLow()
            else:
                self.__setHigh()
