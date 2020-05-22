from Room import Room
import logging
DEBUG = False
LOG = False
path_to_log = 'doors.log'


def main():

    if DEBUG:
        logging.basicConfig(filename=path_to_log, level=logging.DEBUG)
        logging.debug("DEBUG IS EBABLED")
    elif LOG:
        logging.basicConfig(filename=path_to_log, level=logging.INFO)

    Room319 = Room(room=319, floor=3,
                   building='B', host='vtvm.edi.lv', port=1883,
                   command_topic='command', status_topic='status',
                   actuator_pin=25, pin_numbering='BCM',
                   activeState=1)

    Room319.routine_start()


if __name__ == '__main__':

    main()
