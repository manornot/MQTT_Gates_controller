import os
import logging
logger = logging.getLogger('Relay')

if os.name == 'nt':
    from raspberry_pc_debug import gpio
else:
    import RPi.GPIO as gpio


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
        self.states = [self.on, self.off]
        self.state = self.on
        gpio.setwarnings(False)
        gpio.setmode(self.__pin_numbering)
        gpio.setup(self.__pin, gpio.OUT)
        self.setInActive()

    def __setHigh(self):
        gpio.output(self.__pin, gpio.HIGH)

    def __setLow(self):
        gpio.output(self.__pin, gpio.LOW)

    def setActive(self):
        assert self.state in self.states, "initial state is not set"
        logger.debug(f'Setting active')
        if self.state is self.off:
            if self.activeState is Relay.HIGH:
                self.__setHigh()
            else:
                self.__setLow()

    def setInActive(self):
        assert self.state in self.states, "initial state is not set"
        logger.debug(f'Setting inactive')
        if self.state is self.on:
            if self.activeState is Relay.HIGH:
                self.__setLow()
            else:
                self.__setHigh()
