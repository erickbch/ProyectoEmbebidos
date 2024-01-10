import time
import numpy as np
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

frequency = 100 #Hz
period = 1 / frequency #s
periodUs = period * 1000000 #us

dutyCycleMaxReverse = 100 * 1100 / periodUs #dutyCycle of Max Reverse,11.0%
dutyCycleMaxForward = 100 * 1900 / periodUs #dutyCycle of Max Forward,19.0%
dutyCycleStopped = 100 * 1500 / periodUs #dutyCycle of Stopped, 15.0%

portOut = 12 #PIN 32 = PWM0
GPIO.setup(portOut, GPIO.OUT)

salida = GPIO.PWM(portOut, frequency)

# SECUENCIA DE ARRANQUE
salida.start(dutyCycleStopped) #Valor del que partimos
time.sleep(15)

while True:
    #Recorremos unos valores significativos
    #Bucle hacia delante
    for i in np.arange (15.0, 16.0, 0.1):
        salida.ChangeDutyCycle(i)
        print("Ya llegamos a ", i, "%")
        time.sleep(1)
    print("Ya llegamos a 16.0%")
    print("Ahora paramos")

    salida.ChangeDutyCycle(16.0)
    time.sleep(1)

    print("Ahora hacia atrás")
    #Bucle hacia delante
    for i in np.arange (15.0, 13.0, -0.1):
        salida.ChangeDutyCycle(i)
        print("> Ya llegamos a ", i, "%")
        time.sleep(1)
    # print("Ya llegamos a 14.0%")
    # print("Ahora paramos")
    
    salida.ChangeDutyCycle(15.0)
    time.sleep(0.25)
