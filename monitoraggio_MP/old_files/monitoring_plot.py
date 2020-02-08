#!/usr/bin/env python3

# PM monitoring plotting script
# By seba ;)

import serial, time
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import rc


import pandas as pd

import tkinter as tk
from tkinter import filedialog


# FILE GATHERING
root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(title="Select file", filetypes=((".csv files", "*.csv"),("All files", "*.*")))

try:
    # get data from csv
    csv_data = pd.read_csv(file_path, header=4)
    csv_data.info()
    print(csv_data.head())
    print(csv_data.describe())
except Exception as e:
    print(e)
    print("Operation cancelled by the user!")
    exit()


# PLOTTING

# Graph creation
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

#
xs_list = csv_data["Date"]
ys1_list = csv_data["PM2.5"]
ys2_list = csv_data["PM10"]
ax.plot(xs_list, ys1_list, xs_list, ys2_list)
ax.legend(['PM2.5', 'PM10'])


# plot properties
plt.xticks(np.linspace(0, len(xs_list)-1, 10),rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
# Title and labels
plt.title('Monitoraggio del materiale particolato di Pablito e Seba')
plt.xlabel('Time')
plt.ylabel('[\mu g/m^3]')
plt.grid()

plt.show()