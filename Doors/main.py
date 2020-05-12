from Room import Room


def main():
    Room319 = Room(room=319, floor=3,
                   building='B', host='vtvm.edi.lv', port=1883,
                   command_topic='command', status_topic='status',
                   actuator_pin=25, pin_numbering='BCM',
                   activeState=1)

    Room319.routine_start()


if __name__ == '__main__':
    main()
