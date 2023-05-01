# import serial
import csv
import time
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

GRAPH_X_SIZE = 1200


# ser = serial.Serial('COM4', 115200)

time.sleep(2)

y_upper = 300
y_lower = 180

data_buffer = []
recording_idx = 0
recording_count
last_time = time.time()

# ser.write(b'0') #ser.write(ord('0'))

fig, ax = plt.subplots()
ax.set_xlim(0, GRAPH_X_SIZE)
ax.set_ylim(y_lower, y_upper)
line, = ax.plot([], [])
line_data = np.zeros(GRAPH_X_SIZE)

def press(event):
    global y_upper, y_lower, data_buffer
    # print(event.key)
    if event.key == 'left':
        y_upper -= 20
        y_lower += 20
        ax.set_ylim(y_lower, y_upper)
    if event.key == 'right':
        y_upper += 20
        y_lower -= 20
        ax.set_ylim(y_lower, y_upper)
    if event.key == 'up':
        y_upper += 20
        y_lower += 20
        ax.set_ylim(y_lower, y_upper)
    if event.key == 'down':
        y_upper -= 20
        y_lower -= 20
        ax.set_ylim(y_lower, y_upper)

    if event.key == 'm':
        ser.write(b'0')
            
    if event.key == 'n':
        print('saving...')
        with open('data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([x for x in data_buffer])
        print('saved.')
    print(y_upper)
    print(y_lower)

def update_plot(i):
    global line_data, last_time, data_buffer, recording_idx,
            data_points, led_type
    # Read data from the serial port
    data_in = ser.readline()
    data_raw = data_in.decode('utf-8').rstrip()
    if ',' in data_raw: 
        data = np.fromstring(data_raw, sep=',')
        data_points = int(data[0])
        led_type = int(data[1])
        recording_idx = 0
        data_buffer.append(data_raw)
        return line,

    if recording_idx < data_points and not ',' in data_raw:
        recording_idx += 1
        data_buffer.append(data_raw)

    current_time = time.time()
    print(1.0/(current_time-last_time))
    last_time = current_time
    
    data = float(data_raw)
    line_data = np.append(line_data, data)
    line_data = np.delete(line_data, 0)
    line.set_data(np.arange(GRAPH_X_SIZE), line_data)
    return line,

# Bind keyPress Event
fig.canvas.mpl_connect('key_press_event', press)


# Animate the plot
ani = animation.FuncAnimation(fig, update_plot, blit=False, interval=1)

# Show the plot
plt.show()

# ser.close()
