#!/bin/bash
rm *.py
git clone https://github.com/manornot/MQTT_Gates_controller
mv MQTT_Gates_controller/Gates/* ~/gates_controller/
rm -r -f MQTT_Gates_controller/
