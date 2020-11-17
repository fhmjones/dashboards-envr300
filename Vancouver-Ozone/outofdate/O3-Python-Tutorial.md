---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.6.1-dev
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

<!-- #region colab_type="text" id="Af6e84nV4FvG" -->
## Tutorial Part 1
### Importing modules, importing data, plotting timeseries and scatter plots
<!-- #endregion -->

<!-- #region colab_type="text" id="fyF4Y6Zz_6RE" -->

Import the required python modules
<!-- #endregion -->

```python colab={} colab_type="code" id="unUVivdPmhNz"
#import numpy for mathematics
import numpy as np
#import pandas for dataframes
import pandas as pd
#import matplotlib for plotting
from matplotlib import pyplot as plt
#import glob for easier data import
import glob
```

<!-- #region colab_type="text" id="Aeu0GzWZFzRI" -->
Mount your Google Drive to access data files
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 54} colab_type="code" executionInfo={"elapsed": 309, "status": "ok", "timestamp": 1591985663609, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="vLrL2spWA0sM" outputId="a95c932b-969b-4956-dde3-7272e61d19b7"
# from google.colab import drive
# drive.mount('/content/drive')
```

<!-- #region colab_type="text" id="mxnuV0L3AFGo" -->
Import the data and concatenate the files. This takes each file (one year of data), imports each csv file into a pandas dataframe, and creates a new pandas dataframe with five years of data
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 72} colab_type="code" executionInfo={"elapsed": 5135, "status": "ok", "timestamp": 1590013640924, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="JBiBubDeAOOX" outputId="7fc5d8fd-d8f6-4fe7-8434-e47f78660658"
# dfs = pd.read_csv("data\O3_2017.csv")
dfs = pd.read_excel("data\O3_2017.xlsx")

# files = glob.glob("data/O3_2017.csv") 
# dfs = [pd.read_csv(f,index_col=0, parse_dates=['DATE_PST']) for f in files]

all_O3 = dfs 
# all_O3 = pd.concat(dfs) 
```

<!-- #region colab_type="text" id="oStzyJkTIKNb" -->
### Visualize the data tables
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 431} colab_type="code" executionInfo={"elapsed": 393, "status": "ok", "timestamp": 1590014147392, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="cns_GR1ZGAZk" outputId="25690a3d-c257-4bd1-b7c0-1d912f6b56c5"
 all_O3.head()
# dfs.head()
```

<!-- #region colab_type="text" id="-Dk47y7rwb-y" -->
Visualize entry lines 20-30
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 828} colab_type="code" executionInfo={"elapsed": 410, "status": "ok", "timestamp": 1590014723405, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="3UWP8fFOwjTd" outputId="25326195-be63-4f1a-b174-f077e47a5a94"
all_O3.iloc[19:30]
```

```python colab={"base_uri": "https://localhost:8080/", "height": 86} colab_type="code" executionInfo={"elapsed": 337, "status": "ok", "timestamp": 1590014829352, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="N2Yq2JTjRF0x" outputId="125d684b-c907-4629-9ae2-0d71d2ddf3ef"
all_O3.columns
```

<!-- #region colab_type="text" id="iHiq-fsl6QzO" -->
### Visualize the data as a timeseries
<!-- #endregion -->

<!-- #region colab_type="text" id="LVc025nbF9R0" -->
Define a station to analyze
<!-- #endregion -->

```python colab={} colab_type="code" id="KqX5zZ0W_Ohy"
stat_name = 'Agassiz Municipal Hall'
```

<!-- #region colab_type="text" id="xm6cZgUDI9Hj" -->
Select the station from the data
<!-- #endregion -->

```python colab={} colab_type="code" id="MHRSFQqEJS1s"
stat_O3 = all_O3.loc[all_O3.STATION_NAME == stat_name]
stat_O3.columns
```

<!-- #region colab_type="text" id="uBPdeAerJIdt" -->
Plot the ozone values (using pandas plotting)
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 431} colab_type="code" executionInfo={"elapsed": 394, "status": "ok", "timestamp": 1590015124134, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="0M6yOOSxSUhx" outputId="7ff65380-4c5d-42fa-8bad-0bee892e0295"
stat_O3.head()
```

```python colab={"base_uri": "https://localhost:8080/", "height": 236} colab_type="code" executionInfo={"elapsed": 885, "status": "ok", "timestamp": 1590006827080, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="bNF4iMuDJV_9" outputId="15d6145a-641f-446e-9721-872cdf544187"
ax = stat_O3.RAW_VALUE.plot(figsize=(9, 3), color='k')
ax.set_ylabel("O$_3$ [ppb]")
ax.set_xlabel('Date')
ax.set_title(stat_name)
plt.show()
```

<!-- #region colab_type="text" id="g1-1E5CeNG5q" -->
Display only the first year of data
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 253} colab_type="code" executionInfo={"elapsed": 805, "status": "ok", "timestamp": 1590015331768, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="1ZfpMBLCJrjJ" outputId="84610232-9735-4a19-e7f3-2c771363e954"
ax = stat_O3.RAW_VALUE[0:8760].plot(figsize=(9, 3), color='k')
ax.set_ylabel("O$_3$ [ppb]")
ax.set_xlabel('Date')
ax.set_title(stat_name)
plt.show()
```

<!-- #region colab_type="text" id="ZxD9aI6q6Xdp" -->
### Scatter Plotting
<!-- #endregion -->

<!-- #region colab_type="text" id="evu1vX9K5ARz" -->
Plot the ozone values as a scatter plot (using matplotlib)
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 312} colab_type="code" executionInfo={"elapsed": 599, "status": "ok", "timestamp": 1590007574272, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="vrb_rDy6y_TZ" outputId="d37cd728-30c3-4b1b-d65a-d333aeb35200"
plt.scatter(stat_O3.index, stat_O3.RAW_VALUE,s=1)
plt.title(stat_name)
plt.xlabel('Date')
plt.ylabel('O$_3$ [ppb]')
```

<!-- #region colab_type="text" id="hD-Yw5ZK5S7F" -->
That's a lot of data and is hard to visualize, even with smaller dots. Here we import datetime to be able to easily select a month of data to plot
<!-- #endregion -->

```python colab={} colab_type="code" id="cDzMjouP1xB7"
import datetime
```

<!-- #region colab_type="text" id="CFope3FR5d-o" -->
Now we can plot one month of data, January 2016
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 312} colab_type="code" executionInfo={"elapsed": 615, "status": "ok", "timestamp": 1590008105674, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="NYBKoqFy3hTD" outputId="ab73aeb9-86ab-445d-9c7a-f721204a6236"
plt.scatter(stat_O3.index, stat_O3.RAW_VALUE, s=3)
plt.title(stat_name)
plt.xlabel('Date')
plt.ylabel('O$_3$ [ppb]')
plt.xlim([datetime.date(2017, 1, 1), datetime.date(2017, 2, 1)])
```

<!-- #region colab_type="text" id="35xbIhKN5jo6" -->
The date labels don't look good - below we can change the plotting syntax slightly to be able to use fig.autofmt_xdate() which will format the dates for us automatically
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 305} colab_type="code" executionInfo={"elapsed": 881, "status": "ok", "timestamp": 1590008202725, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="3kB_p2RC06TM" outputId="6c949c2c-e3b0-451c-d038-16079d730c4d"
fig, ax = plt.subplots()
ax.scatter(stat_O3.index, stat_O3.RAW_VALUE, s=3)
ax.set_title(stat_name)
ax.set_ylabel('Date')
ax.set_xlabel('O$_3$ [ppb]')
ax.set_xlim([datetime.date(2017, 1, 1), datetime.date(2017, 2, 1)])
fig.autofmt_xdate()
```

<!-- #region colab_type="text" id="BMbDVgfQ6d8b" -->
### Calculate and Visualize the MDA8
<!-- #endregion -->

<!-- #region colab_type="text" id="oxWtAf9iJBMG" -->
Calculate the maximum daily 8 hour average (MDA8) - this measure is often used for regulatory analyses


<!-- #endregion -->

```python colab={} colab_type="code" id="Kl5jIy6gJUIR"
stat_8hr_O3 = stat_O3.RAW_VALUE.rolling(8,min_periods=6).mean()
MDA8_stat=stat_8hr_O3.resample('D').max()
```

<!-- #region colab_type="text" id="er5grK3PJMYt" -->
Plot the MDA8
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 241} colab_type="code" executionInfo={"elapsed": 554, "status": "ok", "timestamp": 1590006867556, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="8zOTW-TOGQp3" outputId="66fccbe4-29c1-46d5-aef6-f02fff078186"
ax = MDA8_stat.plot(figsize=(9, 3), color='k')
ax.set_ylabel("MDA8 O$_3$ [ppb]")
ax.set_xlabel('Date')
ax.set_title(stat_name)
plt.show()
```

```python

```
