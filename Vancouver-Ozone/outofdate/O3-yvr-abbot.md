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

<!-- #region colab_type="text" id="Af6e84nV4FvG" -->
## Tutorial Part 1
### Importing modules, importing data, plotting timeseries and scatter plots
Adapted from [this tutorial](https://drive.google.com/drive/folders/1Tj7pDVd33IKeeKaoKIGzvSiswPft56Tb)

Input data is a modified version of raw because original files are 25-35 MBytes and contain much redundant information. Raw data were adapted to CSV files with only the necessary parts, mainly to (a) speed up input to Python code and (b) avoid the necessary dataframe code that is otherwise needed to extract required data.
<!-- #endregion -->

```python colab={} colab_type="code" id="unUVivdPmhNz"
#import numpy for mathematics, pandas for dataframes, matplotlib for plotting
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
```

```python colab={"base_uri": "https://localhost:8080/", "height": 72} colab_type="code" executionInfo={"elapsed": 5135, "status": "ok", "timestamp": 1590013640924, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="JBiBubDeAOOX" outputId="7fc5d8fd-d8f6-4fe7-8434-e47f78660658"
all_O3 = pd.read_csv("data/YVR and Abbotsford 2017.csv",index_col=0, parse_dates=['date_pst'])
all_O3.head()
```

```python colab={"base_uri": "https://localhost:8080/", "height": 828} colab_type="code" executionInfo={"elapsed": 410, "status": "ok", "timestamp": 1590014723405, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="3UWP8fFOwjTd" outputId="25326195-be63-4f1a-b174-f077e47a5a94"
# Visualize entry lines 20-29
# all_O3.iloc[19:30]
```

```python colab={"base_uri": "https://localhost:8080/", "height": 86} colab_type="code" executionInfo={"elapsed": 337, "status": "ok", "timestamp": 1590014829352, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="N2Yq2JTjRF0x" outputId="125d684b-c907-4629-9ae2-0d71d2ddf3ef"
all_O3.columns
```

<!-- #region colab_type="text" id="iHiq-fsl6QzO" -->
### Visualize the data as a timeseries
<!-- #endregion -->

<!-- #region colab_type="text" id="uBPdeAerJIdt" -->
Using _pandas plotting_ to plot the data as a line graph
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 253} colab_type="code" executionInfo={"elapsed": 805, "status": "ok", "timestamp": 1590015331768, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="1ZfpMBLCJrjJ" outputId="84610232-9735-4a19-e7f3-2c771363e954"
stat_name = 'YVR_ppb'

ax = all_O3.YVR_ppb.plot(figsize=(9, 3), color='k')
ax.set_ylabel("O$_3$ [ppb]")
ax.set_xlabel('Date')
ax.set_title(stat_name)
plt.show()
```

<!-- #region colab_type="text" id="evu1vX9K5ARz" -->
Use _matplotlib_ to plot the data as a scatter plot
<!-- #endregion -->

```python colab={"base_uri": "https://localhost:8080/", "height": 312} colab_type="code" executionInfo={"elapsed": 599, "status": "ok", "timestamp": 1590007574272, "user": {"displayName": "Rivkah Gardner-Frolick", "photoUrl": "", "userId": "01660883882147847432"}, "user_tz": 420} id="vrb_rDy6y_TZ" outputId="d37cd728-30c3-4b1b-d65a-d333aeb35200"
plt.scatter(all_O3.index, all_O3.Abbotsford_ppb, s=1)
plt.title(stat_name)
plt.xlabel('Date')
plt.ylabel('O$_3$ [ppb]')
```

```python
# get the current axis: 
ax = plt.gca()

# This doesn't seem to like mixing line and scatter.

all_O3.plot(kind='line',x='date',y='Abbotsford_ppb', color='red', ax=ax)
all_O3.plot(kind='line',x='date',y='YVR_ppb', ax=ax)

#all_O3.plot(kind='scatter',x='date',y='Abbotsford_ppb', color='red', s=1, ax=ax)
#all_O3.plot(kind='scatter',x='date',y='YVR_ppb',s=1, ax=ax)

plt.show()
```

### Plot smoothed versions of these two data sets
This plot can be made interactive; set smoothing window and which dataset to plot. Or - plot smoothed over raw. This won't be too hard, but overlaying a 'Maximum Daily 8-hr average' plot (below) will be harder.

```python
# rolling n-point moving average (hence the .mean()); data points are 1hr apart, hence 24/day or 168/wk.
days = 7
hrs = 24*days
YVR_smoothed = all_O3.YVR_ppb.rolling(hrs, center=True, min_periods=6).mean() 
Abb_smoothed = all_O3.Abbotsford_ppb.rolling(hrs, center=True, min_periods=6).mean() 

# add this as a column to the dataframe
all_O3['YVR_smoothed']=YVR_smoothed
all_O3['Abb_smoothed']=Abb_smoothed
```

```python
fig, ax = plt.subplots(figsize=(8,4))

all_O3.plot(kind='line',x='date',y='Abb_smoothed', color="red", ax=ax)
all_O3.plot(kind='line',x='date',y='YVR_smoothed', color="blue", ax=ax)
ax.set_ylabel("O$_3$ [ppb]")
ax.set_title(f"Data smoothed over {days} days.")

plt.show()
```

<!-- #region colab_type="text" id="BMbDVgfQ6d8b" -->
### Calculate and Visualize the MDA8
<!-- #endregion -->

<!-- #region colab_type="text" id="oxWtAf9iJBMG" -->
Calculate the maximum daily 8 hour average (MDA8) - this measure is often used for regulatory analyses.

BUT ... to overlay this directly onto the raw data plot is hard because x-axis is different. Don't know how to do this.
<!-- #endregion -->

```python
# rolling 8hr moving "average" (hence the .mean()); points are 1hr apart
app_8hr_O3 = all_O3.Abbotsford_ppb.rolling(8,min_periods=6).mean()
yvr_8hr_O3 = all_O3.YVR_ppb.rolling(8,min_periods=6).mean()
```

```python
# resample result by "day" (the 'D'), choosing the max value. 
MDA8_app=app_8hr_O3.resample('D').max()
MDA8_yvr=yvr_8hr_O3.resample('D').max()
```

```python colab={} colab_type="code" id="Kl5jIy6gJUIR"
# do this similarly to above - get labels, legend, etc. 
# Plot the MDA8 using pandas plotting
ax = MDA8_app.plot(figsize=(9, 3), color='r')
ax = MDA8_yvr.plot(color='b')
ax.set_ylabel("MDA8 O$_3$ [ppb]")
ax.set_xlabel('Date')
ax.set_title('MDA8 of Abb (Red) and YVR(Blue)')
plt.show()
```

```python

```
