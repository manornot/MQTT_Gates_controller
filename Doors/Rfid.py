import time
import binascii
import functools
import os
PN532 = False
RC522 = True

if os.name == 'nt':
    from raspberry_pc_debug import Adafruit_PN532 as PN532
    from raspberry_pc_debug import SimpleMFRC522
else:
    if PN532:
        import Adafruit_PN532 as PN532
    if RC522:
        from mfrc522 import SimpleMFRC522


class RFID_Reader:
    def __init__(self, CS=8, SCLK=11, MOSI=10, MISO=9):
        self.CS = CS
        self.MOSI = MOSI
        self.MISO = MISO
        self.SCLK = SCLK
        if PN532:
            self.P532_reader_init()
        elif RC522:
            self.RC522_reader_init()

    def P532_reader_init(self):
        self.reader = PN532.PN532(cs=self.CS,
                                  sclk=self.SCLK,
                                  mosi=self.MOSI,
                                  miso=self.MISO)
        self.reader.begin()
        self.isActive = self.isActive_PN532
        self.readUID = self.readUID_PN532
        self.writeBlock = self.writeBlock_PN532
        self.readBlock = self.readBlock_PN532
        if self.isActive():
            self.reader.SAM_configuration()

    def isActive_PN532(self):
        _, ver, rev, _ = self.reader.get_firmware_version()
        assert len(ver) > 0, "rfid is dead"
        if ver:
            return True

    def readUID_PN532(self):
        return binascii.hexlify(self.reader.read_passive_target())[2:-1]

    def writeBlock_PN532(self, block, data):
        return self.reader.mifare_classic_write_block(block, data)

    def readBlock_PN532(self, block):
        return self.reader.mifare_classic_read_block(block)

    def RC522_reader_init(self):
        self.reader = SimpleMFRC522()
        self.isActive = self.isActive_RC522
        self.readUID = self.readUID_RC522
        self.writeBlock = self.writeBlock_RC522
        self.readBlock = self.readBlock_RC522

    def isActive_RC522(self):
        status, *_ = self.reader.READER.MFRC522_Anticoll()
        if status != self.reader.READER.MI_OK:
            return False
        if status:
            return True

    def readUID_RC522(self):
        uid = self.reader.read_id_no_block()
        return uid

    def writeBlock_RC522(self, block, write):
        return self.reader.write()

    def readBlock_RC522(self, block):
        *_, data = self.reader.read_no_block()
        return data
