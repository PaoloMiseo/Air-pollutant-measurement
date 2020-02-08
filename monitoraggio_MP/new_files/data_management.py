#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by: Sebastian Peradotto
@Date: 22/01/2020
@Project:
"""

import logging
from datetime import datetime
import csv
import time
from threading import Thread


class DataManagement:
    def __init__(self, *args, **kwargs):
        logging.basicConfig(filename=kwargs.get('logfile_path', None),
                            filemode='a', level=logging.INFO)
        # filename
        self.csv_filename = kwargs.get('filename',
                                       '/home/pi/mu_code/monitoraggio_MP/new_files/monitoring_data/monitoraggio_dati_started_{}.csv'.format(
                                           datetime.now().strftime("%b%d_%H%M%S")))
        self.save = kwargs.get('save', False)
        self.create_csv()

        self.sensor = kwargs.get('sensor', None)
        self.sampling_interval = kwargs.get('sampling_interval', 1000)
        self.data_thread = None

        if not self.data_thread:
            self.create_measurement_thread()

    def create_csv(self):
        if self.save:
            # write csv_header
            with open(self.csv_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Monitoraggio del materiale particolato di Pablito e Seba'])
                writer.writerow(['by Sebastian Peradotto (purosangue)'])

                right_now = datetime.now()
                now_str = right_now.strftime("%b %d %Y %H:%M:%S")

                writer.writerow(['Started at: {date}'.format(date=now_str)])
                writer.writerow(['Data unit: [micro g/m^3]'])
                writer.writerow(['Date', 'PM2.5', 'PM10'])

    def write_data_to_csv(self, data):
        with open(self.csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def get_measurement(self):
        while True:
            right_now, pmtwofive, pmten = self.sensor.get_data()

            # save data
            if self.save:
                self.write_data_to_csv([right_now.strftime("%b %d %Y %H:%M:%S"), pmtwofive, pmten])

            print("PM2.5 = {mp25}, PM10 = {mp10} @{time}".format(mp10=pmten,
                                                                 mp25=pmtwofive,
                                                                 time=right_now.strftime("%H:%M:%S")))

            logging.debug("Sample gathering successful")
            #print("Sample gathering successful")
            # Not very accurate as sampling time
            time.sleep(self.sampling_interval / 1000)

    def create_measurement_thread(self):
        self.data_thread = Thread(name='measurement_thread',
                                  target=self.get_measurement)
        self.data_thread.daemon = True

    def start_measurement(self):
        self.data_thread.start()




