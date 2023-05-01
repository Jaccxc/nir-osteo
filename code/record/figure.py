import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, ifft

fp = open('data.csv', "r", encoding="utf-8")
csv_reader = csv.reader(fp) #解讀資料
data = list(csv_reader) #把資料存成list
type = 0    #分辨三種波段
fp.close()

# with open('data.csv', "r", newline='') as csvfile:
#     rows = csv.reader(csvfile, delimiter='\n')

#     for row in rows:
#         print(row)


for row in data:

    #依據資料判斷波長並建立list
    if row[0] == "1680,5":
        type = 1
        data_810nm = []
    if row[0] == "560,6,":
        type = 2
        data_860nm = []
    if row[0] == "560,7,":
        type = 3
        data_940nm = []

    #將資料加入對應波長的list
    if "," not in row[0]:
        content = float(row[0].replace('ovf', '999'))
        if type == 1:
            data_810nm.append(content)
        if type == 2:
            data_860nm.append(content)
        if type == 3:
            data_940nm.append(content)

#印出
print("810nm:")
print(data_810nm)
# print("860nm:")
# print(data_860nm)
# print("940nm:")
# print(data_940nm)


#畫出折線圖
x = np.linspace(0,60,1680)

fig_810nm = plt.figure(figsize=(24,4), dpi=200)
plt.plot(x, data_810nm,"r",linewidth=0.8)
plt.title("810nm")
fig_810nm.savefig('810nm.png')

# fig_860nm = plt.figure()
# plt.plot(x, data_860nm, "g")
# plt.title("860nm")
# fig_860nm.savefig('860nm.png')

# fig_940nm = plt.figure()
# plt.plot(x, data_940nm, "b")
# plt.title("940nm")
# fig_940nm.savefig('940nm.png')


# #傅立葉轉換
# N = 70
# dt = 10.0/N

# fig = plt.figure(figsize=(15,4), dpi=72)
# yf = fft(data_810nm)
# xf = fftfreq(N, dt)
# plt.plot(xf[:N//4], dt*7.0*np.abs(yf[:N//4]), color='blue')
# plt.grid()
# plt.xlabel('frequency (Hz)', fontsize=14)
# plt.ylabel('intensity', fontsize=14)
# fig.savefig('fft.png')