GPS to MQTT for Chase Cars
==========================

Provides a means of passing a chase car position, or other GPS position, to an MQTT broker.  The position is taken from any GPS receiver that emits GGA sentences over a serial link.


Dependencies
============

This gateway is written in Python and has been tested on a Raspberry Pi.  It should work on any computer that runs Python however.

It uses the [paho-mqtt](https://pypi.org/project/paho-mqtt/) and pyserial libraries:

	pip install paho-mqtt
	python -m pip install pyserial



MQTT
============

You need an MQTT broker to upload the position to.  If needed, a user name and password can be set.



Usage
=======

	python gpt_mqtt.py <gps_device> <chase_callsign> <mqtt_broker> <mqtt_path> [<mqtt_username> <mqtt_password>]

- gps_device: this is the GPS receiver device e.g. /dev/ttyACM0
- chase_callsign: set to whatever callsign you want your position to be uploaded with
- mqtt_broker: this is the hostname or IP address for the MQTT broker that is receiving your telemetry
- mqtt_path: this is the path to the telemetry on the server
- mqtt_username and mqtt_password are only required if your MQTT broker requires them.
