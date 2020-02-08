#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created by: Sebastian Peradotto
@Date: 22/01/2020
@Project: 
"""

# import matplotlib as mpl
# mpl.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc

import numpy as np

import logging


class Plotting:
    def __init__(self, *args, **kwargs):
        logging.basicConfig(filename=kwargs.get('logfile_path', None),
                            filemode='a', level=logging.INFO)
        # Graph Initial Parameters
        self.x_len = kwargs.get('x_len', 25)
        self.y_range = kwargs.get('y_range', [0, 100])
        self.fig = kwargs.get('fig', None)
        self.ax = kwargs.get('ax', None)
        self.sensor = kwargs.get('sensor', None)
        self.plot_sampling_time = kwargs.get('update_time', 2500)
        self.anim = None

        if self.fig is None or self.ax is None:
            self.graph_creation()

        if not self.anim:
            self.create_animation_thread()

    def graph_creation(self):
        logging.info("Graph parameters creation")
        print("Graph parameters creation")
        # Graph creation
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_ylim(self.y_range)

        # Title and labels
        plt.title('Monitoraggio del materiale particolato di Pablito e Seba')
        plt.xlabel('Time')
        plt.ylabel('[\mu g/m^3]')

    def animate(self, i):

        # Populate the data lists
        while not self.sensor.xs.empty():
            self.sensor.xs_list.append(self.sensor.xs.get())
            self.sensor.ys1_list.append(self.sensor.ys1.get())
            self.sensor.ys2_list.append(self.sensor.ys2.get())

        # Extract the min/max values for plot dimensions
        min_val = min(min(self.sensor.ys1_list, self.sensor.ys2_list))
        max_val = max(max(self.sensor.ys1_list, self.sensor.ys2_list))

        self.ax.set_ylim([0.9 * min_val, 1.1 * max_val])

        # Limit the number of elements
        # self.sensor.xs_list = self.sensor.xs_list[-x_len:]
        # self.sensor.ys1_list = self.sensor.ys1_list[-x_len:]
        # self.sensor.ys2_list = self.sensor.ys2_list[-x_len:]

        # axis update
        self.ax.clear()
        self.ax.plot(self.sensor.xs_list, self.sensor.ys1_list, self.sensor.xs_list, self.sensor.ys2_list)
        self.ax.legend(['PM2.5', 'PM10'])

        # plot properties
        plt.xticks(np.linspace(0, len(self.sensor.xs_list) - 1, 10), rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.2)
        plt.title('Monitoraggio del materiale particolato di Pablito e Seba')
        plt.xlabel('Time')
        plt.ylabel('[\mu g/m^3]')
        plt.grid()

        logging.debug("Graph update successful")
        #print("Graph update successful")

    def create_animation_thread(self):
        self.anim = FuncAnimation(self.fig, self.animate,
                                  frames=200, interval=self.plot_sampling_time)

    @staticmethod
    def start_animation():
        plt.show()










