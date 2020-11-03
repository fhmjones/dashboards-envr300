## Ozone at YVR and Abbotsford

**Objectives**: to plot 1) either raw dataset or both; 2) either 7-day avg, or both, 3) either maximum daily 8-hr avg, or both; 4) do this with dashboard and plotly.


```python
# intro to figurewidgets at https://plotly.com/python/figurewidget/import numpy as np

import pandas as pd
# matplotlib needed only for checking data early during design
from matplotlib import pyplot as plt

import plotly
import plotly.graph_objects as go
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode(connected = True)

import ipywidgets as widgets
from ipywidgets import interact
```

```python
# read in the data from the prepared CSV file. 
all_O3 = pd.read_csv("data/YVR and Abbotsford 2017.csv",index_col=0, parse_dates=['date_pst'])
# all_O3.head()
# all_O3.columns
```

```python
# rolling n-point moving average (hence the .mean()); data points are 1hr apart, hence 24/day or 168/wk.
days = 7
hrs = 24*days
YVR_smoothed = all_O3.YVR_ppb.rolling(hrs, center=True, min_periods=6).mean() 
Abb_smoothed = all_O3.Abbotsford_ppb.rolling(hrs, center=True, min_periods=6).mean() 

# add this as columns to the dataframe
all_O3['YVR_smoothed']=YVR_smoothed
all_O3['Abb_smoothed']=Abb_smoothed

# all_O3['Abb_smoothed']
```

```python
# rolling 8hr moving "average" (hence the .mean()); points are 1hr apart
yvr_8hr_O3 = all_O3.YVR_ppb.rolling(8,min_periods=6).mean()
abb_8hr_O3 = all_O3.Abbotsford_ppb.rolling(8,min_periods=6).mean()

# abb_8hr_O3[:20]
```

```python
# resample result by "day" (the 'D'), choosing the max value. 
YVR_max8hrsavg=yvr_8hr_O3.resample('D').max()
Abb_max8hrsavg=abb_8hr_O3.resample('D').max()

# tried to add this as columns to the dataframe
# BUT DOESN'T WORK BECAUSE THERE IS ONLY ONE POINT PER DAY, NOT 24. 
# all_O3['YVR_max8hrsavg']=YVR_max8hrsavg
# all_O3['Abb_max8hrsavg']=Abb_max8hrsavg

# YVR_max8hrsavg
```

```python
# Test by plotting MDA8 using pandas plotting

#ax = YVR_max8hrsavg.plot(figsize=(9, 4), color='g')
#ax = Abb_max8hrsavg.plot(color='c')
#ax = YVR_smoothed.plot(color='b')
#ax = Abb_smoothed.plot(color='r')
#ax.set_ylabel("MDA8 O$_3$ [ppb]")
#ax.set_xlabel('Date')
#ax.set_title('MDA8 of YVR(Blue) and Abb (Red)')

# plt.show()
```

```python
# first define the dashboard controls or "widget objects"
# YVR = Vancouver airport
# Abb = Abbotsford
# MDA8 = maximum daily 8 hour average

YVR_raw = widgets.Checkbox(
    value=True,
    description='YVR Raw',
    disabled=False,
    indent=False
)
Abb_raw = widgets.Checkbox(
    value=False,
    description='Abb Raw',
    disabled=False,
    indent=False
)
YVR_smooth = widgets.Checkbox(
    value=False,
    description='YVR smooth',
    disabled=False,
    indent=False
)
Abb_smooth = widgets.Checkbox(
    value=False,
    description='Abb smooth',
    disabled=False,
    indent=False
)
YVR_mda8 = widgets.Checkbox(
    value=False,
    description='YVR MDA8',
    disabled=False,
    indent=False
)
Abb_mda8 = widgets.Checkbox(
    value=False,
    description='Abb MDA8',
    disabled=False,
    indent=False
)

#containers not useful when using the "decorator" approach to interactive widgets. 
#container1 = widgets.VBox(children=[YVR_raw, Abb_raw])
#container2 = widgets.VBox(children=[YVR_MDA8, Abb_MDA8])
```

```python
# Build the figure

g = go.FigureWidget()

g.layout.width = 900
g.layout.height = 500
g.layout.xaxis.title = 'Date'
g.layout.yaxis.title = 'Amplitude'

#g.add_scatter(x=all_O3.index, y=all_O3.YVR_smoothed, mode="lines", line=dict(color='blue'), name="YVR smooth")
#g.add_scatter(x=all_O3.index, y=all_O3.YVR_max8hrsavg, mode="lines", line=dict(color='green'), name="YVR mda8")

#g
```

```python
# function to handle input from the widgets, and alter the state of the graph
# for use of decorator `@interact` see https://plotly.com/python/v3/interact-decorator/
# find line parameters at https://plotly.com/python/line-charts/ 
# find color names at https://www.w3schools.com/colors/colors_names.asp
# find "clear graph or trace" at https://community.plotly.com/t/remove-all-traces/13469 

@interact(YVR_raw = True, Abb_raw = True, YVR_smooth = False, Abb_smooth = False, YVR_mda8 = False, Abb_mda8 = False)
def update(YVR_raw, Abb_raw, YVR_smooth, Abb_smooth, YVR_mda8, Abb_mda8):
    g.data = []           # clear the graph
    g.layout.title = ""   # clear the title
    
    if YVR_raw:
        g.add_scatter(x=all_O3.index, y=all_O3.YVR_ppb, mode="lines", 
                      line=dict(color='MediumTurquoise'), name="YVR")
        g.layout.title = "YVR"
    if Abb_raw:
        g.add_scatter(x=all_O3.index, y=all_O3.Abbotsford_ppb, mode="lines", 
                      line=dict(color='SandyBrown'), name="Abb")
        g.layout.title = "Abb"
    if YVR_smooth:
        g.add_scatter(x=all_O3.index, y=all_O3.YVR_smoothed, mode="lines", 
                      line=dict(color='green'), name="YVR smooth")
        g.layout.title = "YVR"
    if Abb_smooth:
        g.add_scatter(x=all_O3.index, y=all_O3.Abb_smoothed, mode="lines", 
                      line=dict(color='red'), name="Abb smooth")
        g.layout.title = "Abb"
    if YVR_mda8:
        g.add_scatter(x=YVR_max8hrsavg.index, y=YVR_max8hrsavg, mode="lines", 
                      line=dict(color='blue', width=2), name="YVR mda8")
        g.layout.title = "YVR"
    if Abb_mda8:
        g.add_scatter(x=YVR_max8hrsavg.index, y=Abb_max8hrsavg, mode="lines", 
                      line=dict(color='firebrick', width=2), name="Abb mda8")
        g.layout.title = "Abb"

    if (YVR_raw or YVR_smooth or YVR_mda8) and (Abb_raw or Abb_smooth or Abb_mda8):
        g.layout.title = "YVR and Abb"

g

# Problem with this version is I'm not sure we can build containors to format the dashboard. 
```

```python

```

```python

```
