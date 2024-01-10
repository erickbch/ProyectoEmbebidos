frequency = 100 #Hz
period = 1 / frequency #s
periodUs = period * 1000000 #us
dutyCycleMaxReverse = 100 * 1100 / periodUs #dutyCycle of Max Reverse,11.0%
dutyCycleMaxForward = 100 * 1900 / periodUs #dutyCycle of Max Forward,19.0%
dutyCycleStopped = 100 * 1500 / periodUs #dutyCycle of Stopped, 15.0%
