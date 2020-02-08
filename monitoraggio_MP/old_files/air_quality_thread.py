#!/usr/bin/env python3

import serial
import time
import numpy as np
#import matplotlib as mpl
#mpl.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc

from datetime import datetime

from threading import Thread
import queue
import csv

import sys
sys.stdout.flush()


import logging
logging.basicConfig(filename='/home/pi/mu_code/monitoring.log', filemode='w', level=logging.DEBUG)
# Scritto da Sebastian Peradotto, il purosangue, per Pablito

logging.info("Attempt to connect to the sensor")
print("Attempt to connect to the sensor")

try:
    # Create the serial port
    ser = serial.Serial('/dev/ttyUSB0')
    logging.info("Connection Successful")
    print("Connection Successful")
except Exception as e:
    print(e)
    logging.critical("Ciao Pablito: The sensor is possibly not connected. Check the connection and try again!")
    exit()



logging.info("Creating global variables")
print("Creating global variables")

# Data Sampling Time
# 10 min -> 600000 ms
data_sampling_time = 1000#ms

# Graphical Sampling Time
plot_sampling_time = 2.5*data_sampling_time #ms

# filename
csv_filename = '/home/pi/mu_code/monitoraggio_dati_started_{}.csv'.format(datetime.now().strftime("%b%d_%H%M%S"))
save = True

if save:
    # write csv_header
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Monitoraggio del materiale particolato di Pablito e Seba'])
        writer.writerow(['by Sebastian Peradotto (purosangue)'])

        now = datetime.now()
        now_str = now.strftime("%b %d %Y %H:%M:%S")

        writer.writerow(['Started at: {date}'.format(date=now_str)])
        writer.writerow(['Data unit: [micro g/m^3]'])
        writer.writerow(['Date','PM2.5','PM10'])


logging.info("Graph parameters creation")
print("Graph parameters creation")
# Graph Initial Parameters
x_len = 25
y_range = [0, 100]

# Graph creation
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.set_ylim(y_range)

# Title and labels
plt.title('Monitoraggio del materiale particolato di Pablito e Seba')
plt.xlabel('Time')
plt.ylabel('[\mu g/m^3]')

logging.info("Creation of queues for thread information sharing")
print("Creation of queues for thread information sharing")

# Queues for data sampling
xs = queue.Queue()
ys1 = queue.Queue()
ys2 = queue.Queue()

logging.info("Function and thread definitions")
print("Function and thread definitions")

def write_data_to_csv(data):
    global csv_filename
    with open(csv_filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def get_sensor_data():
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little')/10
    pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little')/10


    return pmtwofive, pmten

def populate_queue(xs, ys1, ys2, sampling_interval):
    while True:
        now = datetime.now()
        pmtwofive, pmten = get_sensor_data()

        # Assuming xs, ys1 and ys2 are Queues objects
        xs.put(now.strftime("%H:%M:%S"))
        ys1.put(pmtwofive) #pm2.5
        ys2.put(pmten) #pm10

        # save data
        if save:
            write_data_to_csv([now.strftime("%b %d %Y %H:%M:%S"), pmtwofive, pmten])

        print("PM2.5 = {mp25}, PM10 = {mp10} @{time}".format(mp10=pmten,
                                                              mp25=pmtwofive,
                                                              time=now.strftime("%H:%M:%S")))

        logging.debug("Sample gathering successful")
        print("Sample gathering successful")
        # Not very accurate as sampling time
        time.sleep(sampling_interval/1000)


xs_list = []
ys1_list = []
ys2_list = []
def animate(i, xs, ys1, ys2):
    global xs_list, ys1_list, ys2_list

    # Populate the data lists
    while not xs.empty():
        xs_list.append(xs.get())
        ys1_list.append(ys1.get())
        ys2_list.append(ys2.get())

    # Extract the min/max values for plot dimensions
    min_val = min(min(ys1_list,ys2_list))
    max_val = max(max(ys1_list,ys2_list))

    ax.set_ylim([0.9*min_val,1.1*max_val])

    # Limit the number of elements
    #xs_list = xs_list[-x_len:]
    #ys1_list = ys1_list[-x_len:]
    #ys2_list = ys2_list[-x_len:]

    # axis update
    ax.clear()
    ax.plot(xs_list, ys1_list, xs_list, ys2_list)
    ax.legend(['PM2.5', 'PM10'])


    # plot properties
    plt.xticks(np.linspace(0,len(xs_list)-1,10), rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2)
    plt.title('Monitoraggio del materiale particolato di Pablito e Seba')
    plt.xlabel('Time')
    plt.ylabel('[\mu g/m^3]')
    plt.grid()

    logging.debug("Graph update successful")
    print("Graph update successful")


logging.info("Variable instantiation and program start")
print("Variable instantiation and program start")

anim = FuncAnimation(fig, animate, fargs=(xs,ys1,ys2,),
                                frames=200, interval=plot_sampling_time)

data_thread = Thread(name='data_thread',
                         target=populate_queue,
                         args=(xs, ys1, ys2, data_sampling_time, ))
data_thread.daemon = True
data_thread.start()

plt.show()

logging.info("Program start")
print("Program start")





# Buon divetimento Pablito!
# Seba