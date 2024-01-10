# imports del GPS
import serial
import time
import string
import pynmea2
import serial,time
import paho.mqtt.publish as publish
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# imports de la temperatura y humedad
import sys
import Adafruit_DHT

destino = "192.168.98.226" #¡OJO, CAMBIA! IP de Carlota
puerto = 1883

client = mqtt.Client("client")
client.connect(destino, puerto)

# Primero el del GPS

while True:
        try:
              port="/dev/ttyAMA0"
              ser=serial.Serial(port, baudrate=9600, timeout=0.5)
              dataout=pynmea2.NMEAStreamReader()
              newdata=ser.readline()
  
              var1 = 'GNGGA'
  
              if newdata[1:6].decode('utf-8') == var1:
  
                      data_split = newdata.decode('utf-8').split(",")
                      latitud = data_split[2]
                      longitud = data_split[4]
                      grados_latitud = latitud[0:2]
                      grados_longitud = longitud[0:3]
                      lat = float(latitud[2:])/60 + float(grados_latitud)
                      lng = float(longitud[3:])/60 + float(grados_longitud)
                      lng = -lng
                      dataJSON = json.dumps({"latitud": lat,
                      "longitud": lng,
                      "name": "Barco",
                      "icon": "ship",
                      "iconColor": "purple"})
                      print("DataJSON: " + dataJSON)
                      client.publish("siluro/control/gps", dataJSON)
                      client.publish("siluro/control/gps-red",dataJSON)
                      
# Ahora el de humedad y temperatura

sensor_args = { '11': Adafruit_DHT.DHT11,'22': Adafruit_DHT.DHT22,'2302': Adafruit_DHT.AM2302 }

if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
sensor = sensor_args[sys.argv[1]]
pin = sys.argv[2]
else:
print('Usage: sudo ./Adafruit_DHT.py[11|22|2302] <GPIO pin number>')
print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
sys.exit(1)

# Try to grab a sensor reading. Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32
# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

if humidity is not None and temperature is not
None:
#print('Temperatura={0:0.1f}º,
Humedad={1:0.1f}%'.format(temperature, humidity))
dataJSON2 = json.dumps({"temperatura": round(temperature, 3), "humedad": round(humidity,3)})
print("DataJSON2: " + dataJSON2)
client.publish("siluro/sensores",dataJSON2)
else:
print('Failed to get reading. Try again!')
sys.exit(1)
except:
print('Volviendo a intentar...')
