# La navegación que está programada tendría el
siguiente recorrido
##################################################################
                        #
---                                                         #
                        #     |
|                                                           #
                        #     |
|                                                           #
                        #     |
|                                                           #
                        #
|                                                           #
                        #
|                                                           #
                        #     |
^                                                       #
                        #     |
|                                                       #
                        #     |
|                                                       #
                        #
---                                                        #
##################################################################

# CÓDIGO DEL SENSOR DE ULTRASONIDOS
import RPi.GPIO as GPIO
import time
##### MQTT
import paho.mqtt.client as mqtt
import threading
#### VARIABLES DE CONDUCCIÓN
frequency = 100
pwmAnclado = 14.0
pwmAvante = 15.0
pwmCiar = 13.0
pwmizq = pwmAnclado
pwmder = pwmAnclado
tAvante = 15
tGiro = 5
stop = True
manual = True

def on_connect(client, userdata, flags, rc): # The callback for when the client connects to the broker
print("Connected with result code {0}".format(str(rc))) #Print result of connection attempt
client.subscribe("siluro/control/#")
def on_message(client, userdata, msg): # The callback for when a PUBLISH message is received from the server.
print("Message received-> " + msg.topic + " " + str(msg.payload)) # Print a received msg
          if msg.topic =="siluro/control/stop":
              if int(msg.payload.decode('utf-8')) == 1:
                  global stop
                  stop=True
                  pwmder = pwmAnclado
                  pwmizq = pwmAnclado
          elif msg.topic =="siluro/control/manual":
              global manual
              if int(msg.payload.decode('utf-8')) == 1:
                      #global manual
                      manual=True
                      pwmder = pwmAnclado
                      pwmizq = pwmAnclado
                      # 0 - Autónomo | 1- Manual
          elif int(msg.payload.decode('utf-8')) == 0:
                      #global manual
                      manual = False
                      contManual = 0
###################################
def envio():
        pwmizq = pwmAnclado
        pwmder = pwmAnclado
        stop = True
        contador = 0
        t = 0
        global manual
        contManual = 0
        # Empezamos parados
        salidader.ChangeDutyCycle(pwmAnclado)
        salidaizq.ChangeDutyCycle(pwmAnclado)
        time.sleep(0.3)
        print("DutyCicle del motor derecho actual: ", pwmAnclado)
        print("DutyCicle del motor izquierdo actual: ", pwmAnclado)
        #Contenemos el código principal en un aestructura try para limpiar los GPIO al terminar o presentarse un error
        try:
            while True:
            #Implementamos un loop infinito
                  while manual != True:
                        if stop == True:
                            print("> Parando motores")
                            stop = False
                        else:
                                ##################
                                ## NAVEGACIÓN ##
                                ##################
                                # Continua hacia delante
                                print("> AVANTE")
                                pwmder = pwmAvante
                                pwmizq = pwmAvante
                                t = tAvante
                                # Cambia de dirección
                                salidader.ChangeDutyCycle(pwmder)
                                salidaizq.ChangeDutyCycle(pwmizq)
                                time.sleep(t)

                                contador += 1

                                if contador % 2 == 1:
                                    # Giramos hacia la derecha
                                    print("> Girando hacia la derecha...")
                                    # Cambia de dirección
                                    pwmder = pwmAnclado
                                    pwmizq = pwmAvante
                                    t = tGiro
                                else:
                                    # Giramos hacia la
                                    izquierda
                                    print("> Girando hacia la izquierda...")
                                    # Cambia de dirección
                                    pwmder = pwmAvante
                                    pwmizq = pwmAnclado
                                    t = tGiro
                            # Cambia de dirección
                            salidader.ChangeDutyCycle(pwmder)
                            salidaizq.ChangeDutyCycle(pwmizq)
                            time.sleep(t)
                            print(" DutyCicle del motor derecho actual: ", pwmder)
                            print(" DutyCicle del motor izquierdo actual: ", pwmizq)
                      if contManual == 0:
                            print("> MODO MANUAL ACTIVADO")
                            salidader.ChangeDutyCycle(pwmder)
                            salidaizq.ChangeDutyCycle(pwmizq)
                            time.sleep(t)
                            print(" DutyCicle del motor derecho actual: ", pwmder)
                            print(" DutyCicle del motor izquierdo actual: ", pwmizq)
                            contManual+=1
              finally:
                # Reiniciamos todos los canales de GPIO.
                GPIO.cleanup()
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
      client.on_connect = on_connect # Define callback function for successful connection
      client.on_message = on_message # Define callback function for receipt of a message
      client.connect('192.168.97.226', 1883)
      x = threading.Thread(target=envio)
      x.start()
      client.loop_forever()
