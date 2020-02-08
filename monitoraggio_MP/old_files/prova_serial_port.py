import serial.tools.list_ports
import time

while True:
    ser_list = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print(ser_list)
    time.sleep(2.2)