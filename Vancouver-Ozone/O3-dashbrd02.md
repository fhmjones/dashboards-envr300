## Ozone at YVR and Abbotsford

**Objectives**: Plot two data sets with any combination of raw data, 7-day avg, or maximum daily 8-hr avg. Note that YVR = Vancouver airport, Abb = Abbotsford and MDA8 = maximum daily 8 hour average. 

* Select what to display using checkboxes.
* To zoom, pan, examine datapoint values, etc., use controls in the graph's upper right (visible when your mouse is in the graph).
* To zoom to a small time-window along the x-axis, click-and-hold in the dataset to start, then drag and release to set the end of the window. Move this window up and down the axis using the "Pan" button, or reset using the "Reset axes" button (i.e. the little **"home"** icon).

```python
# More detailed development comments are in the "O3-dashbrd01" version of this app. 
# intro to figurewidgets at https://plotly.com/python/figurewidget/
```

```python
import pandas as pd

import plotly
import plotly.graph_objects as go
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode(connected = True)

import ipywidgets as widgets
```

```python
# read in the data from the prepared CSV file. 
# Data are assumed to be in the custom formatted CSV file `YVR and Abbotsford 2017.csv`, stored in the folder `data`. 

all_O3 = pd.read_csv("data/YVR and Abbotsford 2017.csv",index_col=0, parse_dates=['date_pst'])
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
```

```python
# rolling 8hr moving "average" (hence the .mean()); points are 1hr apart
yvr_8hr_O3 = all_O3.YVR_ppb.rolling(8,min_periods=6).mean()
abb_8hr_O3 = all_O3.Abbotsford_ppb.rolling(8,min_periods=6).mean()
```

```python
# resample result by "day" (the 'D'), choosing the max value. 
YVR_max8hrsavg=yvr_8hr_O3.resample('D').max()
Abb_max8hrsavg=abb_8hr_O3.resample('D').max()

# tried to add these as columns to the dataframe BUT ...
# THAT ISN'T EASY BECAUSE THERE IS ONLY ONE POINT PER DAY, NOT 24.
# But they still plot with other traces so long as the correct x-axis is used later in "g.add_scatter"
```

```python
# Define the dashboard controls or "widget objects"
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

#containers for orgnaizing the dashboard 
container1 = widgets.VBox(children=[YVR_raw, YVR_smooth, YVR_mda8])
container2 = widgets.VBox(children=[Abb_raw, Abb_smooth, Abb_mda8])
container3 = widgets.HBox(children=[container1, container2])
```

```python
# Build the figure
# first a blank figurewidget object, then specify fixed parameters. 

g = go.FigureWidget()

g.layout.width = 900
g.layout.height = 500
g.layout.xaxis.title = 'Date'
g.layout.yaxis.title = 'Amplitude'
```

```python
# plot one dataset when first run ...
g.add_scatter(x=all_O3.index, y=all_O3.YVR_ppb, mode="lines", 
                      line=dict(color='MediumTurquoise'), name="YVR raw")

# function to handle input from the widgets, and alter the state of the graph
# find line parameters at https://plotly.com/python/line-charts/ 
# find color names at https://www.w3schools.com/colors/colors_names.asp

def response(change):
    g.data = []           # clear the graph
    g.layout.title = ""   # clear the title
    
    if YVR_raw.value:
        g.add_scatter(x=all_O3.index, y=all_O3.YVR_ppb, mode="lines", 
                      line=dict(color='MediumTurquoise'), name="YVR raw")
        g.layout.title = "Vancouver Airport"
    if Abb_raw.value:
        g.add_scatter(x=all_O3.index, y=all_O3.Abbotsford_ppb, mode="lines", 
                      line=dict(color='SandyBrown'), name="Abb raw")
        g.layout.title = "Abbotsford"
    if YVR_smooth.value:
        g.add_scatter(x=all_O3.index, y=all_O3.YVR_smoothed, mode="lines", 
                      line=dict(color='green'), name="YVR 7-day average")
        g.layout.title = "Vancouver Airport"
    if Abb_smooth.value:
        g.add_scatter(x=all_O3.index, y=all_O3.Abb_smoothed, mode="lines", 
                      line=dict(color='red'), name="Abb 7-day average")
        g.layout.title = "Abbotsford"
    if YVR_mda8.value:  # different "x" because mda8 has daily values, not hourly values. 
        g.add_scatter(x=YVR_max8hrsavg.index, y=YVR_max8hrsavg, mode="lines", 
                      line=dict(color='blue', width=2), name="YVR max daily 8hr avg")
        g.layout.title = "Vancouver Airport"
    if Abb_mda8.value:
        g.add_scatter(x=YVR_max8hrsavg.index, y=Abb_max8hrsavg, mode="lines", 
                      line=dict(color='firebrick', width=2), name="Abb max daily 8hr avg")
        g.layout.title = "Abbotsford"

    if (YVR_raw.value or YVR_smooth.value or YVR_mda8.value) and (Abb_raw.value or Abb_smooth.value or Abb_mda8.value):
        g.layout.title = "Vancouver Airport and Abbotsford"

# interacting with a widget causes the `observe` method to call back to the `response` function to update the plot
# "observe" is explained https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html#Arguments-that-are-dependent-on-each-other
# it is probably not the most straight forward approach, although it seems to work. 
# Next steps (below) should be to clean this up. 
YVR_raw.observe(response, names="value")
Abb_raw.observe(response, names="value")
YVR_smooth.observe(response, names="value")
Abb_smooth.observe(response, names="value")
YVR_mda8.observe(response, names="value")
Abb_mda8.observe(response, names="value")
```

```python
# organize the dashboard widgets and plot

widgets.VBox([container3, g])
```

```python
# NEXT: pursue more informed use of widgets using "interact" widget functionality more carefully. 
# See https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html, including ...
# use of "observe" to handle arguments that are dependent on each other.
# There are also guidelines for using "display" and "interactive_output" to manage layout. 
```

## Usage for teaching and learning
Here are just a few examples of questions that could be posed in class, on your own, or as an assignment. Choices will depend on whether this dashboard is being used to compare ozone levels at a coastal location to those further inland, or whether the purpose is to explore the challenges and potential for working with "messy" data sets. 
1. Plot just one raw data set. How much variation is there over the whole year? 
2. Use zoom and scrolling functionality to estimate daily variability of this parameter. 
3. What times during the year seem to have lowest ozone levels? Highest Ozone levels? How difficult is it to make these judgements 
4. Plot two raw data sets. Which site appears to experience higher ozone events? At what time of year? Why might that be? 
5. Are ozone variations easier to "see" by processing data with a 7-day average or by calcuating the maximum daily 8-hr average? 
6. Which of these two processing options makes it easier (or more effective) to compare these two stations stations? Why? 
7. Look closely at a day or two of smoothed and mda8 data. You should see they appear to be not quite "lined up". Why is this? _{{Because smoothed values are hourly wherease mda8 is a daily value assigned to the date at "0" hours. So the mda8 peak may not match up with a smoothed hourly peak. Most daily peaks are in the afternoon, especially in the summer.}}_
8. many other ideas ...

---


## Attribution
* Data used here are hourly ozone (parts per billion) for 2017 only, from 2 of many monitoring stations. Full datasets can be found at the BC Data Catalogue, [Air Quality Monitoring: Verified Hourly Data](https://catalogue.data.gov.bc.ca/dataset/77eeadf4-0c19-48bf-a47a-fa9eef01f409), licensed under the [Open Government Licence – British Columbia](https://www2.gov.bc.ca/gov/content/data/open-data/open-government-licence-bc). For more information about these data and their source, see the [Status of Ground-Level Ozone in B.C. (2015-2017)](http://www.env.gov.bc.ca/soe/indicators/air/ozone.html) web page.
* The idea is derived from a discussion between Tara Ivanochko and Rivkah Gardner-Frolick <rivkahgf@gmail.com> who uses the complete dataset as part of a [Python tutorial](https://colab.research.google.com/drive/1DO0ICvInsr74vnl3AcPBoGtJyNrV-J8F?usp=sharing#scrollTo=a5l7UD_njHPv) on importing modules, importing data, plotting timeseries and scatter plots.
* Code by [Francis Jones](https://www.eoas.ubc.ca/people/francisjones).
