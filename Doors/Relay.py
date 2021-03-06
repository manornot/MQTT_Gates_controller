import os
import logging
logger = logging.getLogger('Relay')
try:

    if os.name == 'nt':
        from raspberry_pc_debug import gpio
    else:
        import RPi.GPIO as gpio
except:
    pass


class Relay:
    HIGH = True
    LOW = False

    def __init__(self, pin, pin_numbering, activeState):
        logger.debug(
            f'pin = {pin}, pin_numbering = {pin_numbering}, activeState = {activeState}')
        self.__pin = pin
        self.__pin_numbering = gpio.BCM if pin_numbering is 'BCM' else gpio.BOARD
        self.activeState = activeState
        self.off = not self.activeState
        self.on = self.activeState
        gpio.setwarnings(False)
        gpio.setmode(self.__pin_numbering)
        gpio.setup(self.__pin, gpio.OUT)
        self.states = [self.on, self.off]
        self.state = self.getState()
        self.setInActive()

    def __setHigh(self):
        gpio.output(self.__pin, gpio.HIGH)

    def __setLow(self):
        gpio.output(self.__pin, gpio.LOW)

    def setActive(self):
        assert self.state in self.states, "initial state is not set"
        logger.debug(f'Setting active')
        logger.debug(self)
        if self.state is self.off:
            if self.activeState is Relay.HIGH:
                self.__setHigh()
            else:
                self.__setLow()
        self.state = self.getState()

    def setInActive(self):
        assert self.state in self.states, "initial state is not set"
        logger.debug(f'Setting inactive')
        logger.debug(self)
        if self.state is self.on:
            if self.activeState is Relay.HIGH:
                self.__setLow()
            else:
                self.__setHigh()
        self.state = self.getState()

    def getState(self):
        logger.debug(f'pin state = {gpio.input(self.__pin)}')
        logger.debug(
            f'self.activeState ^ bool(gpio.input(self.__pin)) = {self.activeState ^ bool(gpio.input(self.__pin))}')
        return self.off if self.activeState ^ bool(gpio.input(self.__pin)) else self.on

    def __str__(self):
        return f'active state = {self.activeState}, off state = {self.off}, on state = {self.on}, available states = {self.states}, current state = {self.state}'
