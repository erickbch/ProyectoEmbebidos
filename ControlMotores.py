import RPi.GPIO as GPIO
import time
import numpy as np

##### MQTT
import paho.mqtt.client as mqtt
import threading

frequency = 100
pwmder = 14.0
pwmizq = 14.0
stop = True
motorder = 5000
motorizq = 5000
rangoMandos = 10000
minNormalizado = 12.0
maxNormalizado = 16.0
rangoNormalizado = maxNormalizado - minNormalizado

def on_connect(client, userdata, flags, rc): # The callback for when the client connects to the broker
print("Connected with result code {0}".format(str(rc))) #Print result of connection attempt client.subscribe("siluro/control/#")

def on_message(client, userdata, msg): # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload)) # Print a received msg
    if msg.topic =="siluro/control/motorder":
        global motorder
        motorder= int(msg.payload.decode('utf-8'))
    elif msg.topic =="siluro/control/motorizq":
        global motorizq
        motorizq= int(msg.payload.decode('utf-8'))
    elif msg.topic =="siluro/control/stop":
        if int(msg.payload.decode('utf-8')) == 1:
            global stop
            stop=True
            motorizq = 5000
            motorder = 5000
###################################
def envio():
        pwmizq = 14.0
        pwmder = 14.0
        stop = True
        print('Iniciando motores...')
        while(True):
              if stop == True:
                  stop = False
              else:
                  #motor izquierdo
                  if 4995<=motorizq<=5005:
                      pwmizq = 14.0 #ms
                  elif motorizq>=5500:
                      pwmizq = (motorizq * rangoNormalizado / rangoMandos) + minNormalizado
                  elif motorizq<4500:
                      pwmizq = (motorizq * rangoNormalizado / rangoMandos) + minNormalizado
                  #motor derecho
                  if 4995<=motorder<=5005:
                      pwmder = 14.0 #ms
                  elif motorder>=5500:
                      pwmder = (motorder * rangoNormalizado / rangoMandos) + minNormalizado
                  elif motorder<=4500:
                      pwmder = (motorder * rangoNormalizado / rangoMandos) + minNormalizado
              salidader.ChangeDutyCycle(pwmder)
              salidaizq.ChangeDutyCycle(pwmizq)
              time.sleep(0.3)
              print("DutyCicle del motor derecho actual: ", pwmder)
              print("DutyCicle del motor izquierdo actual: ", pwmizq)
              print("Motor derecho sin normalizar: ", motorder)
              print("Motor derecho sin normalizar: ", motorizq)
################# "main"
if __name__ == "__main__":
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        portOutDer = 12 #PIN32 = PWM0
        GPIO.setup(portOutDer, GPIO.OUT)
        portOutIzq = 13 #PIN33 = PWM1
        GPIO.setup(portOutIzq, GPIO.OUT)

        salidader = GPIO.PWM(portOutDer, frequency)
        salidaizq = GPIO.PWM(portOutIzq, frequency)
        salidader.start(pwmder) #Valor del que partimos
        salidaizq.start(pwmizq)

        client = mqtt.Client("client")
        client.on_connect = on_connect # Define callback function for
        successful connection
        client.on_message = on_message # Define callback function for
        receipt of a message
        client.connect('192.168.232.226', 1883)

        x = threading.Thread(target=envio)
        x.start()

        client.loop_forever()
