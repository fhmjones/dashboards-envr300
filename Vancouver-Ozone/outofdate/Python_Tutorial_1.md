---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.7.0-rc0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region id="Af6e84nV4FvG" colab_type="text" -->
## Tutorial Part 1
### Importing modules, importing data, plotting timeseries and scatter plots
<!-- #endregion -->

<!-- #region id="fyF4Y6Zz_6RE" colab_type="text" -->

Import the required python modules
<!-- #endregion -->

```python id="unUVivdPmhNz" colab_type="code" colab={}
#import numpy for mathematics
import numpy as np
#import pandas for dataframes
import pandas as pd
#import matplotlib for plotting
from matplotlib import pyplot as plt
#import glob for easier data import
import glob
```

<!-- #region id="Aeu0GzWZFzRI" colab_type="text" -->
Mount your Google Drive to access data files
<!-- #endregion -->

```python id="vLrL2spWA0sM" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 54} executionInfo={"status": "ok", "timestamp": 1591985663609, "user_tz": 420, "elapsed": 309, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="a95c932b-969b-4956-dde3-7272e61d19b7"
from google.colab import drive
drive.mount('/content/drive')
```

<!-- #region id="mxnuV0L3AFGo" colab_type="text" -->
Import the data and concatenate the files. This takes each file (one year of data), imports each csv file into a pandas dataframe, and creates a new pandas dataframe with five years of data
<!-- #endregion -->

```python id="JBiBubDeAOOX" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 72} executionInfo={"status": "ok", "timestamp": 1590013640924, "user_tz": 420, "elapsed": 5135, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="7fc5d8fd-d8f6-4fe7-8434-e47f78660658"
files = glob.glob("drive/My Drive/O3_*.csv")
dfs = [pd.read_csv(f,index_col=0, parse_dates=['DATE_PST']) for f in files]

all_O3 = pd.concat(dfs)
```

<!-- #region id="oStzyJkTIKNb" colab_type="text" -->
###Visualize the data tables
<!-- #endregion -->

```python id="cns_GR1ZGAZk" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 431} executionInfo={"status": "ok", "timestamp": 1590014147392, "user_tz": 420, "elapsed": 393, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="25690a3d-c257-4bd1-b7c0-1d912f6b56c5"
all_O3.head()
```

<!-- #region id="-Dk47y7rwb-y" colab_type="text" -->
Visualize entry lines 20-30
<!-- #endregion -->

```python id="3UWP8fFOwjTd" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 828} executionInfo={"status": "ok", "timestamp": 1590014723405, "user_tz": 420, "elapsed": 410, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="25326195-be63-4f1a-b174-f077e47a5a94"
all_O3.iloc[19:30]
```

```python id="N2Yq2JTjRF0x" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 86} executionInfo={"status": "ok", "timestamp": 1590014829352, "user_tz": 420, "elapsed": 337, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="125d684b-c907-4629-9ae2-0d71d2ddf3ef"
all_O3.columns
```

<!-- #region id="iHiq-fsl6QzO" colab_type="text" -->
### Visualize the data as a timeseries
<!-- #endregion -->

<!-- #region id="LVc025nbF9R0" colab_type="text" -->
Define a station to analyze
<!-- #endregion -->

```python id="KqX5zZ0W_Ohy" colab_type="code" colab={}
stat_name = 'Agassiz Municipal Hall'
```

<!-- #region id="xm6cZgUDI9Hj" colab_type="text" -->
Select the station from the data
<!-- #endregion -->

```python id="MHRSFQqEJS1s" colab_type="code" colab={}
stat_O3 = all_O3.loc[all_O3.STATION_NAME == stat_name]

```

<!-- #region id="uBPdeAerJIdt" colab_type="text" -->
Plot the ozone values (using pandas plotting)
<!-- #endregion -->

```python id="0M6yOOSxSUhx" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 431} executionInfo={"status": "ok", "timestamp": 1590015124134, "user_tz": 420, "elapsed": 394, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="7ff65380-4c5d-42fa-8bad-0bee892e0295"
stat_O3.head()
```

```python id="bNF4iMuDJV_9" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 236} executionInfo={"status": "ok", "timestamp": 1590006827080, "user_tz": 420, "elapsed": 885, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="15d6145a-641f-446e-9721-872cdf544187"
ax = stat_O3.RAW_VALUE.plot(figsize=(9, 3), color='k')
ax.set_ylabel("O$_3$ [ppb]")
ax.set_xlabel('Date')
ax.set_title(stat_name)
plt.show()
```

<!-- #region id="g1-1E5CeNG5q" colab_type="text" -->
Display only the first year of data
<!-- #endregion -->

```python id="1ZfpMBLCJrjJ" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 253} executionInfo={"status": "ok", "timestamp": 1590015331768, "user_tz": 420, "elapsed": 805, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="84610232-9735-4a19-e7f3-2c771363e954"
ax = stat_O3.RAW_VALUE[0:8760].plot(figsize=(9, 3), color='k')
ax.set_ylabel("O$_3$ [ppb]")
ax.set_xlabel('Date')
ax.set_title(stat_name)
plt.show()
```

<!-- #region id="ZxD9aI6q6Xdp" colab_type="text" -->
### Scatter Plotting
<!-- #endregion -->

<!-- #region id="evu1vX9K5ARz" colab_type="text" -->
Plot the ozone values as a scatter plot (using matplotlib)
<!-- #endregion -->

```python id="vrb_rDy6y_TZ" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 312} executionInfo={"status": "ok", "timestamp": 1590007574272, "user_tz": 420, "elapsed": 599, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="d37cd728-30c3-4b1b-d65a-d333aeb35200"
plt.scatter(stat_O3.index, stat_O3.RAW_VALUE,s=1)
plt.title(stat_name)
plt.xlabel('Date')
plt.ylabel('O$_3$ [ppb]')
```

<!-- #region id="hD-Yw5ZK5S7F" colab_type="text" -->
That's a lot of data and is hard to visualize, even with smaller dots. Here we import datetime to be able to easily select a month of data to plot
<!-- #endregion -->

```python id="cDzMjouP1xB7" colab_type="code" colab={}
import datetime
```

<!-- #region id="CFope3FR5d-o" colab_type="text" -->
Now we can plot one month of data, January 2016
<!-- #endregion -->

```python id="NYBKoqFy3hTD" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 312} executionInfo={"status": "ok", "timestamp": 1590008105674, "user_tz": 420, "elapsed": 615, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="ab73aeb9-86ab-445d-9c7a-f721204a6236"
plt.scatter(stat_O3.index, stat_O3.RAW_VALUE, s=3)
plt.title(stat_name)
plt.xlabel('Date')
plt.ylabel('O$_3$ [ppb]')
plt.xlim([datetime.date(2016, 1, 1), datetime.date(2016, 2, 1)])
```

<!-- #region id="35xbIhKN5jo6" colab_type="text" -->
The date labels don't look good - below we can change the plotting syntax slightly to be able to use fig.autofmt_xdate() which will format the dates for us automatically
<!-- #endregion -->

```python id="3kB_p2RC06TM" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 305} executionInfo={"status": "ok", "timestamp": 1590008202725, "user_tz": 420, "elapsed": 881, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="6c949c2c-e3b0-451c-d038-16079d730c4d"
fig, ax = plt.subplots()
ax.scatter(stat_O3.index, stat_O3.RAW_VALUE, s=3)
ax.set_title(stat_name)
ax.set_ylabel('Date')
ax.set_xlabel('O$_3$ [ppb]')
ax.set_xlim([datetime.date(2016, 1, 1), datetime.date(2016, 2, 1)])
fig.autofmt_xdate()
```

<!-- #region id="BMbDVgfQ6d8b" colab_type="text" -->
### Calculate and Visualize the MDA8
<!-- #endregion -->

<!-- #region id="oxWtAf9iJBMG" colab_type="text" -->
Calculate the maximum daily 8 hour average (MDA8) - this measure is often used for regulatory analyses


<!-- #endregion -->

```python id="Kl5jIy6gJUIR" colab_type="code" colab={}
stat_8hr_O3 = stat_O3.RAW_VALUE.rolling(8,min_periods=6).mean()
MDA8_stat=stat_8hr_O3.resample('D').max()
```

<!-- #region id="er5grK3PJMYt" colab_type="text" -->
Plot the MDA8
<!-- #endregion -->

```python id="8zOTW-TOGQp3" colab_type="code" colab={"base_uri": "https://localhost:8080/", "height": 241} executionInfo={"status": "ok", "timestamp": 1590006867556, "user_tz": 420, "elapsed": 554, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}} outputId="66fccbe4-29c1-46d5-aef6-f02fff078186"
ax = MDA8_stat.plot(figsize=(9, 3), color='k')
ax.set_ylabel("MDA8 O$_3$ [ppb]")
ax.set_xlabel('Date')
ax.set_title(stat_name)
plt.show()
```
