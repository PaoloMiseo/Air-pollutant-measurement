#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created by: Sebastian Peradotto
@Date: 22/01/2020
@Project: Monitoraggio del materiale particolato
"""

# Scritto da Sebastian Peradotto, il purosangue, per Pablito

from plotting import Plotting
from pm_sensor import PMsensor
from data_management import DataManagement

import sys
import logging

# Get console output
sys.stdout.flush()

# Logger
logfile_path = '/home/pi/mu_code/monitoraggio_MP/new_files/monitoring_data/monitoring.log'
logging.basicConfig(filename=logfile_path, filemode='w', level=logging.INFO)


# Data Sampling Time
# 10 min -> 600000 ms
data_sampling_time = 1000  # ms

# Graphical Sampling Time
plot_sampling_time = 2.5*data_sampling_time  # ms

# filename
save = True
#filename = '/home/pi/mu_code/monitoring_file.csv'

if __name__ == '__main__':

    pm_sens = PMsensor(connect=True,
                       logfile_path=logfile_path)
    data_manage = DataManagement(save=save,
                                 sensor=pm_sens,
                                 sampling_interval=data_sampling_time,
                                 logfile_path=logfile_path)
    plot = Plotting(sensor=pm_sens,
                    update_time=plot_sampling_time)

    data_manage.start_measurement()
    plot.start_animation()


# Buon divetimento Pablito!
# Seba