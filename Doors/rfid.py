import time
import binascii
import functools
PN532 = False
RC522 = True
if PN532:
    import Adafruit_PN532 as PN532
if RC522:
    from mfrc522 import SimpleMFRC522


class RFID_Reader:
    def P532_reader_init(self):
        self.reader = PN532.PN532(cs=self.CS,
                                  sclk=self.SCLK,
                                  mosi=self.MOSI,
                                  miso=self.MISO)
        self.reader.begin()

        if self.isActive():
            self.reader.SAM_configuration()

    def RC522_reader_init(self):
        self.reader = SimpleMFRC522()

    def __init__(self, CS=8, SCLK=11, MOSI=10, MISO=9):
        self.CS = CS
        self.MOSI = MOSI
        self.MISO = MISO
        self.SCLK = SCLK
        if PN532:
            P532_reader_init()
        elif RC522:
            RC522_reader_init()

    @isActive_RC522
    def isActive(self):
        _, ver, rev, _ = self.reader.get_firmware_version()
        assert len(ver) > 0, "rfid is dead"
        if ver:
            return True

    @readUID_RC522
    def readUID(self):
        return binascii.hexlify(self.reader.read_passive_target())[2:-1]

    @writeBlock_RC522
    def writeBlock(self, block, data):
        return self.reader.mifare_classic_write_block(block, data)

    @readBlock_RC522
    def readBlock(self, block):
        return self.reader.mifare_classic_read_block(block)

    def readUID_RC522(self, read):
        if RC522:
            @functools.wraps(read)
            def wrapper(*args):
                return self.reader.read()
            return wrapper
        return read

    def writeBlock_RC522(self, read):
        if RC522:
            @functools.wraps(read)
            def wrapper(*args):
                return self.reader.read()
            return wrapper
        return read

    def readBlock_RC522(self, read):
        if RC522:
            @functools.wraps(read)
            def wrapper(*args):
                return self.reader.read()
            return wrapper
        return read

    def isActive_RC522(self, read):
        (status, uid) = self.reader.READER.MFRC522_Anticoll()
        if status != self.reader.READER.MI_OK:
            return False
        if status:
            return True
