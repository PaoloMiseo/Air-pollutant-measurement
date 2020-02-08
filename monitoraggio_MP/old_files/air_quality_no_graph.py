
import serial, time


ser = serial.Serial('/dev/ttyUSB0')


def get_sensor_data():
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little')/10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little')/10
    return pmtwofive, pmten

while True:

    pmtwofive, pmten = get_sensor_data()
    print("PM2.5 = {mp25}, PM10 = {mp10}".format(mp10=pmten, mp25=pmtwofive))

    time.sleep(1)