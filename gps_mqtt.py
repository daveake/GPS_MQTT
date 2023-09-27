import paho.mqtt.client as mqtt
import sys
import time
import serial
import math

def FixPosition(Position):
    Position = Position / 100
    MinutesSeconds = math.modf(Position)
    return MinutesSeconds[1] + MinutesSeconds[0] * 5 / 3

def ProcessLine(Line):
    Fields = Line.split(',')
    
    if len(Fields) > 10:
        if Fields[0][3:6] == "GGA":
            if (Fields[1] != '') and (len(Fields[2]) >= 6):
                # Got time and position
                Time = Fields[1][:2] + ':' + Fields[1][2:4] + ':' + Fields[1][4:6]
                Latitude = FixPosition(float(Fields[2]))
                if Fields[3] == 'S':
                    Latitude = -Latitude
                    
                Longitude = FixPosition(float(Fields[4]))
                if Fields[5] == 'W':
                    Longitude = -Longitude
                    
                Altitude = float(Fields[9])
                Sats = int(Fields[7])
                
                return {'time': Time, 'lat': "%.5f" % Latitude, 'lon': "%.5f" % Longitude, 'alt': "%.f" % Altitude, 'sats': Sats}
                
    return None

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    
def PublishPositionToMQTT(Position):
    mqttc = mqtt.Client("python_chase")
    
    mqttc.on_publish = on_publish    
    
    if len(sys.argv) > 6:
        mqttc.username_pw_set(sys.argv[5], sys.argv[6]) 
    
    print("Connecting to mqtt broker " + sys.argv[3])
    
    mqttc.connect(sys.argv[3], 1883)
    
    print("Connected to mqtt broker " + sys.argv[3])
    
    res = mqttc.publish(sys.argv[4] + '/' + sys.argv[2], str(Position))

    mqttc.disconnect()
    
    return res[0] == 0
    
    
if len(sys.argv) < 5:
    print ("Usage: python gpt_mqtt.py <gps_device> <chase_callsign> <mqtt_broker> <mqtt_path> [<mqtt_username> <mqtt_password>]")
    quit()    
    
ser = serial.Serial()
ser.baudrate = 9600
ser.stopbits = 1
ser.bytesize = 8
ser.timeout = 0
ser.port = sys.argv[1]

ser.open()
Line = ''
Position = None

while True:
    # Do incoming characters
    Byte = ser.read(1)
    
    if len(Byte) > 0:
        Character = chr(Byte[0])

        if len(Line) > 256:
            Line = ''
        elif Character != '\r':
            if Character == '\n':
                # print(Line)
                NewPosition = ProcessLine(Line)
                if NewPosition:
                    Position = NewPosition
                                   
                Line = ''
                time.sleep(0.01)
            else:
                Line = Line + Character
    elif Position:
        print(Position)
        if PublishPositionToMQTT(Position):
            Position = None
    else:
        time.sleep(0.01)
    
