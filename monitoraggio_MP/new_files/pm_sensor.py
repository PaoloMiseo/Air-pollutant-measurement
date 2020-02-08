#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by: Sebastian Peradotto
@Date: 22/01/2020
@Project:
"""

import logging
import queue
from datetime import datetime


class PMsensor:
    def __init__(self, *args, **kwargs):
        logging.basicConfig(filename=kwargs.get('logfile_path', None),
                            filemode='a', level=logging.INFO)

        self.open_serial_port = kwargs.get('connect', True)
        self.use_test_func = kwargs.get('test_function', False)
        self.func = self.select_function()

        # Queues for data sampling
        self.xs = queue.Queue()
        self.ys1 = queue.Queue()
        self.ys2 = queue.Queue()

        self.xs_list = []
        self.ys1_list = []
        self.ys2_list = []

        if self.open_serial_port:
            self.serial_port = self.sensor_connect()
        else:
            self.serial_port = None


    @staticmethod
    def sensor_connect():
        import serial

        logging.info("Attempt to connect to the sensor")
        print("Attempt to connect to the sensor")

        try:
            # Create the serial port
            ser = serial.Serial('/dev/ttyUSB0')
            logging.info("Connection Successful")
            print("Connection Successful")
            return ser
        except Exception as e:
            print(e)
            logging.critical("Ciao Pablito: The sensor is possibly not connected. Check the connection and try again!")
            print("Ciao Pablito: The sensor is possibly not connected. Check the connection and try again!")
            exit()

    def get_sensor_data(self):
        data = []
        for index in range(0, 10):
            datum = self.serial_port.read()
            data.append(datum)

        now = datetime.now()
        pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
        pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

        # Assuming xs, ys1 and ys2 are Queues objects
        self.xs.put(now.strftime("%H:%M:%S"))
        self.ys1.put(pmtwofive)  # pm2.5
        self.ys2.put(pmten)  # pm10

        return now, pmtwofive, pmten

    def get_sensor_data(self):
        data = []
        for index in range(0, 10):
            datum = self.serial_port.read()
            data.append(datum)

        now = datetime.now()
        pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
        pmten = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

        # Assuming xs, ys1 and ys2 are Queues objects
        self.xs.put(now.strftime("%H:%M:%S"))
        self.ys1.put(pmtwofive)  # pm2.5
        self.ys2.put(pmten)  # pm10

        return now, pmtwofive, pmten

    def get_data(self):
        return self.func()

    def select_function(self):
        if self.use_test_func:
            return self.test_func
        else:
            return self.get_sensor_data

    def test_func(self):
        import random
        data = []

        now = datetime.now()
        pmtwofive = random.randint(0,100)
        pmten = random.randint(0,100)

        # Assuming xs, ys1 and ys2 are Queues objects
        self.xs.put(now.strftime("%H:%M:%S"))
        self.ys1.put(pmtwofive)  # pm2.5
        self.ys2.put(pmten)  # pm10

        return now, pmtwofive, pmten