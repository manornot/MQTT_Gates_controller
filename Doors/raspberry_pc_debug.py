import random
import numpy as np


class gpio:
    OUT = 1
    IN = 0
    HIGH = 1
    LOW = 0
    BCM = 1
    BOARD = 0

    def setmode(self, *args):
        pass

    def output(self, *args):
        pass

    def input(self, *args):
        return 1

    def setup(self, *args):
        pass

    def setwarnings(self, *args):
        pass


class Adafruit_PN532:
    class PN532:
        def __init__(self, **kwargs):
            pass

        def begin(self):
            pass

        def get_firmware_version(self):
            return 1, '1', '1', 1

        def SAM_configuration(self):
            pass

        def read_passive_target(self):
            return bytes(str(np.random.rand(10)), 'utf-8')


class mfrc522:
    pass


class SimpleMFRC522(mfrc522):
    pass
