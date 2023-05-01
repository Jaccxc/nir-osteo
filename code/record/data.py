import serial
import csv
import time
import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt

N = 1680

ser = serial.Serial('COM5', 115200)

time.sleep(5)

ser.write(b'0') #ser.write(ord('0'))

with open('data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in range((N+1)+1):
        data_in = ser.readline()
        data_raw = data_in.decode('utf-8')
        print(data_raw)
        light = data_raw[0:6]

        writer.writerow([light])
ser.close()
