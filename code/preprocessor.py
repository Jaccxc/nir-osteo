import csv
import numpy as np
import matplotlib.pyplot as plt
from skimage.restoration import denoise_wavelet
from scipy.fft import fft, fftfreq, ifft

fp = open('810nm_data.csv', "r", encoding="utf-8")
csv_reader = csv.reader(fp) #解讀資料
data = list(csv_reader) #把資料存成list
type = 0    #分辨三種波段
fp.close()

for row in data:
    #依據資料判斷波長並建立list
    if row[0] == "70,5,0":
        type = 1
        data_810nm = []
    if row[0] == "70,6,0":
        type = 2
        data_860nm = []
    if row[0] == "70,7,0":
        type = 3
        data_940nm = []

    #將資料加入對應波長的list
    if "," not in row[0]:
        if type == 1:
            data_810nm.append(float(row[0]))
        if type == 2:
            data_860nm.append(float(row[0]))
        if type == 3:
            data_940nm.append(float(row[0]))


#----------------- PREPROCESSING -----------------# 

wave_bias = np.mean(data_810nm)

data_810nm_no_bias = data_810nm - wave_bias

#--------------- FOURIER TRANSFORM ---------------# 

#傅立葉轉換
N = 70
sampling_freq = 28.0
dt = 1.0/(sampling_freq)

yf = fft(data_810nm_no_bias)
xf = fftfreq(N, dt)

#---------------- ANALYTIC VERBOSE ---------------# 

main_idx = np.argmax(np.abs(yf[:N//2]))
main_freq = xf[:N//2][main_idx]
main_mag = np.abs(yf[main_idx])

print(f"Main component frequency: {main_freq:.2f} Hz")
print(f"Main component magnitude: {main_mag:.2f}")

#------------------ RECONSTRUCT ------------------# 

top_n_component = 10
idx = np.argsort(np.abs(yf[:N//2]))[::-1][:top_n_component]
yf_filt = np.zeros_like(yf)
yf_filt[:N//4] = yf[:N//4]

signal_filt_fourier = ifft(yf_filt).real
signal_filt_fourier += wave_bias

wavelet_level = 2
signal_filt_wavelet = denoise_wavelet(data_810nm_no_bias, method='BayesShrink', mode='soft', 
                        wavelet_levels=wavelet_level, wavelet='sym8', rescale_sigma='True')

#--------------------- PLOT ----------------------# 

fig, ax = plt.subplots(5, 1, figsize=(8, 6))
x = np.linspace(0,10,70)

current_plot = ax[0]
current_plot.plot(x, data_810nm, label="Original")
plt.setp(current_plot, xlabel='Time')
plt.setp(current_plot, ylabel='Light Intensity')
current_plot.set_title('Original Wave', loc="left", pad=-3)

current_plot = ax[1]
current_plot.plot(xf[:N//2], dt*np.abs(yf[:N//2]), color='blue')
plt.setp(current_plot, xlabel='Frequency (Hz)')
plt.setp(current_plot, ylabel='Intensity')
current_plot.set_title(f'Original FFT Analytic', loc="left", pad=-3)

current_plot = ax[2]
current_plot.plot(x, signal_filt_fourier, label="Reconstructed (Fourier top {top_n_component} components)")
plt.setp(current_plot, xlabel='Time')
plt.setp(current_plot, ylabel='Light Intensity')
current_plot.set_title(f'FFT Top {top_n_component} Component Reconstructed', loc="left", pad=-3)

current_plot = ax[3]
current_plot.plot(xf[:N//2], dt*np.abs(yf_filt)[:N//2], label="Reconstructed Fourier  Analytic", color='blue')
plt.setp(current_plot, xlabel='Frequency (Hz)')
plt.setp(current_plot, ylabel='Intensity')
current_plot.set_title(f'Reconstructed Fourier top {top_n_component} Analytic', loc="left", pad=-3)

current_plot = ax[4]
current_plot.plot(x, signal_filt_wavelet, label="Reconstructed (Wavelet Level {})")
plt.setp(current_plot, xlabel='Time')
plt.setp(current_plot, ylabel='Light Intensity')
current_plot.set_title(f'Wavelet Level {wavelet_level} Component Reconstructed', loc="left", pad=-3)


fig.tight_layout()

plt.show()