
import serial, time
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc
from datetime import datetime

ser = serial.Serial('/dev/ttyUSB0')


sampling_time = 2190 #ms

# Graph Parameters
x_len = 25
y_range = [0, 100]

# Graph creation
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_ylim(y_range)

# Title and labels
plt.title('Monitoraggio del materiale particolato di Pablito')
plt.xlabel('Time')
plt.ylabel('[\mu g/m^3]')

# Lists to display
xs = []
ys1 = []
ys2 = []

# Create display line
#line1, = ax.plot(xs, ys1, lw=3)
#line2, = ax.plot(xs, ys2, lw=3)

def get_sensor_data():
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little')/10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little')/10
    return pmtwofive, pmten


def animate(i, xs, ys1, ys2):

    pmtwofive, pmten = get_sensor_data()
    now = datetime.now()

    xs.append(now.strftime("%H:%M:%S"))
    ys1.append(pmtwofive) #pm2.5
    ys2.append(pmten) #pm10

    # Limit the number of elements
    #ys1 = ys1[-x_len:]
    #ys2 = ys2[-x_len:]

    min_val = min(min(ys1,ys2))
    max_val = max(max(ys1,ys2))

    ax.set_ylim([0.9*min_val,1.1*max_val])


    # axis update
    ax.clear()
    ax.plot(xs, ys1, xs, ys2)
    ax.legend(['PM2.5', 'PM10'])


    # plotm properties
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Monitoraggio del materiale particolato di Pablito')
    plt.xlabel('Time')
    plt.ylabel('[\mu g/m^3]')
    plt.grid()


    print("PM2.5 = {mp25}, PM10 = {mp10}".format(mp10=pmten, mp25=pmtwofive))


anim = FuncAnimation(fig, animate, fargs=(xs,ys1,ys2,),
                            frames=200, interval=sampling_time)

plt.show()