"""
We create sensor data for 5 sensors.
There is 24hrs of data for each sensor.
The time is recorded in seconds.
The start time is different for each sensor but
is within ~2 hours of 6am of may 1, 2023.
"""

#|%%--%%| <emuOpc2Yc4|9Y7ozZnvoi>

import datetime as dt
import numpy as np
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors

#|%%--%%| <9Y7ozZnvoi|XzPfsoKRhg>

#-Create the timeseries data-----------------------
data = {}
for i in range(5):
    ts_x = np.hstack((0, np.random.normal(0, 2, 3600 * 24 - 1)))
    ts_y = np.hstack((0, np.random.normal(0, 2, 3600 * 24 - 1)))
    ts_z = np.hstack((0, np.random.normal(0, 2, 3600 * 24 - 1)))
    ts_dic = {'x': ts_x, 'y': ts_y, 'z': ts_z}
    data[f'sensor_{i}'] = pd.DataFrame(ts_dic)

sensors = data.keys()

#|%%--%%| <XzPfsoKRhg|KvwqbMMfgY>

for k in data.keys():
    for col in data[k].columns:
        sen_data = data[k][col]
        # constant freqs
        dom = np.linspace(0, 1, sen_data.size)
        freq_no = np.random.randint(75, 100 + 1) * (sen_data.size / (60 * 5))
        freq = np.sin(2 * np.pi * dom * freq_no)
        data[k][col] += freq
        freq_no = np.random.randint(30, 50 + 1) * (sen_data.size / (60 * 5))
        freq = np.sin(2 * np.pi * dom * freq_no)
        data[k][col] += freq

#|%%--%%| <KvwqbMMfgY|lQsVxsmLNk>

def spectrogram(signal, period_len=60 * 5):
    freqs = np.fft.rfftfreq(period_len, d=1 / period_len)
    len_thresh = signal.size // period_len
    signal = signal[: period_len * len_thresh].reshape((-1, period_len))
    ffts = np.abs(np.fft.rfft(signal, axis=1))
    return freqs, ffts

def plot_spectrogram_mpl(freqs, ffts, show=False):
    t = np.linspace(0, ffts.shape[0] - 1, ffts.shape[0])
    xx, yy = np.meshgrid(t, freqs)
    fig, ax = plt.subplots()
    ax.pcolormesh(xx, yy, ffts.T,
                  shading='auto',
                  norm=colors.Normalize(ffts.min(), ffts.max()),
                  cmap=plt.cm.viridis)
    if show:
        return plt.show()
    else:
        return fig, ax

#|%%--%%| <lQsVxsmLNk|JRTks6czMC>

fig, ax = plt.subplots(1, 3)
for i, col in enumerate(data['sensor_1'].columns):
    ax[i].plot(data['sensor_1'][col].values)
plt.show()

fq, ft = spectrogram(data['sensor_1']['x'].values)
plot_spectrogram_mpl(fq, ft, show=True)

#|%%--%%| <JRTks6czMC|O9sdIE69OJ>
#--------------------------------------------------
time_stamps = {}
for i in range(5):
    del_t = np.random.normal(2, 1)
    hr = int(del_t)
    min = int((del_t - int(del_t)) * 60)
    t_start = dt.datetime(2023, 5, 1, 6 + hr, min, 0)
    ts = t_start.timestamp() + np.arange(0, 24 * 3600, 60)
    time_stamps[sensors[i]] = ts.astype(int)
time_stamps = pd.DataFrame(time_stamps)

lat_lon = {}
for sensor in sensors:
    lat = 300 + np.random.normal(0, 10)
    lon = 200 + np.random.normal(0, 6)
    lat_lon[sensor] = np.array([lat, lon]).T
lat_lon = pd.DataFrame(lat_lon, index=['lat', 'lon'])
#--------------------------------------------------

# Open connection to the database
connection = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='',
    port=3306,
    database='sensor_data'
)
#--------------------------------------------------

#-Create the tables-------------------------------
cursor = connection.cursor()
sql_code = "CREATE TABLE IF NOT EXISTS sensor_names( "
sql_code += "name_id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, "
sql_code += "name VARCHAR(255) NOT NULL,"
sql_code += "lat VARCHAR(255) DEFAULT NULL,"
sql_code += "lon VARCHAR(255) DEFAULT NULL);"
cursor.execute(sql_code)
connection.commit()
#--------------------------------------------------

for sen in sensors:
    cursor = connection.cursor()
    sql_code = "INSERT INTO sensor_names (name) "
    sql_code += f"SELECT '{sen}' FROM DUAL "
    sql_code += "WHERE NOT EXISTS (SELECT * FROM  sensor_names "
    sql_code += f"WHERE name='{sen}' LIMIT 1);"
    cursor.execute(sql_code)
    connection.commit()


#|%%--%%| <O9sdIE69OJ|wAMMLFoiP7>



