from Room import Room
import logging
logger = logging.getLogger()
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "=[%(levelname)s @ %(filename)s (L=%(lineno)s) F=%(funcName)s() ]= %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.disabled = True


def main():
    Room319 = Room(room=319, floor=3,
                   building='B', host='vtvm.edi.lv', port=1883,
                   command_topic='command', status_topic='status',
                   actuator_pin=25, pin_numbering='BCM',
                   activeState=1)

    Room319.routine_start()


if __name__ == '__main__':
    main()
