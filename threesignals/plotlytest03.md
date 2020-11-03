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

## Signal components, with smoothing.

```python
# Comemnts so they don't show up when run in Voila
# - See plotlytest01 for first attempts. That worked but didn't work in Voila.
# - Version plotlytest02 succeeds in the demo without the smoothing option.
# - This version (plotlytest03) is cleaned up a bit, and adds smoothing. 
# - However it is stuck using a two-trace plot, so "no smoothing" means the smoothed trace is shown as zero. 
# - In other words I haven't figured out how to NOT plot one of the traces. 

# This dasboard starts with information shown in the dashboard explaining the purpose of the dashboard.
```

### Purpose
Demonstrate a synthetic signal consisting of _data + random noise + a linear trend_. Also show effect of smoothing the noisy signal. 

### Instructions
- Explore the dashboard and its controls. 
- Note that figure-viewing controls in the figure's top-right corner only appear when your mouse is within the figure. 

```python
import plotly
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode(connected = True)
import numpy as np
from numpy import random
import math #needed for definition of pi
import ipywidgets as widgets
```

```python
# First assign the widgets

ncycles = widgets.FloatSlider(
    min=1, max=10, step=0.25, value=2.0, description='Num. cycles'
)

noiselevel = widgets.FloatSlider(
    min=0, max=5, step=0.25, value=1.0, description='Noise'
)

# signal
draw_s = widgets.Checkbox(
    value=True,
    description='Sine wave',
    disabled=False,
    indent=True
)

# smoothed result
draw_m = widgets.Checkbox(
    value=False,
    description='Smoothed',
    disabled=False,
    indent=True
)

# random noise series
draw_r = widgets.Checkbox(
    value=True,
    description='Random noise',
    disabled=False,
    indent=True
)

# trend line
draw_t = widgets.Checkbox(
    value=True,
    description='Trend line',
    disabled=False,
    indent=True
) 

# Begin to define the layout of the dashboard. The Vbox puts three checkboxes in a column. 
container1 = widgets.VBox(children=[draw_s, draw_r, draw_t, draw_m]) 
```

```python
# The smoothing function
# Discussion on options for moving avg. are at: 
# https://stackoverflow.com/questions/14313510/how-to-calculate-moving-average-using-numpy
# "convolve" is quick and avoids going to pandas dataframes. However, using Pandas is probably better. 

def moving_avg(x, w):
    y = np.convolve(x, np.ones(w), 'valid') / w
    
    # applying "roll" is necessary so the timeseries are aligned over the correct x-axis values. 
    # this is probably easier using data frames when x-axis will be the index frame.
    z = np.roll(y, int(w/2))
    
    # roll wraps end points back to first points, so set these to zero; a cludge, but works for now.
    z[:2] = 0
    return z
```

```python
# build the X-axis first, then the three time series: 

xpoints = np.arange(0, ncycles.value, 0.05)
N=len(xpoints)         #this may not be the most sophisticated approach 
ypoints = np.sin(xpoints*2*math.pi)
randpoints = noiselevel.value * (random.rand(N)-.5)
trendpoints = 0.4*xpoints + 0.5

# The trace to display is a sum of the three components. 
# Turn components on or off by multiplying by the binary values returned by check box widgets: "component.value". 
# The smoothed result is a separate time series. 
sumpoints = draw_s.value*ypoints + draw_r.value*randpoints + draw_t.value*trendpoints
smoothpoints = draw_m.value*moving_avg(sumpoints,5)

# The 'traces' for the figure are defined as scatter plots, of type "lines".
trace0 = go.Scatter(x=xpoints, y=sumpoints, mode="lines", name="signal")
trace1 = go.Scatter(x=xpoints, y=smoothpoints, mode="lines", name="smoothed")

# Now build the figure and define non-default parameters for this figure
g = go.FigureWidget(data=[trace0, trace1], 
                    layout=go.Layout(title=dict(text='Sinewave+trend+noise & 5-point moving average')))
g.layout.width = 700
g.layout.height = 450
g.layout.xaxis.title = 'x axis'
g.layout.yaxis.title = 'Amplitude'
g.layout.xaxis.range=[0.,11.]
g.layout.yaxis.range=[-4.,8.]
```

```python
# function to handle input from the widgets, and alter the state of the graph
# I think this works by having the "observe" functions monitor the widgets and 
#   generate the calls back to the "response" function.

def response(change):   
    xpoints = np.arange(0, ncycles.value, 0.05)
    N=len(xpoints)         #this may not be the most sophisticated approach 
    ypoints = np.sin(xpoints*2*math.pi)
    randpoints = noiselevel.value * (random.rand(N)-.5)
    trendpoints = 0.4*xpoints + 0.5

    sumpoints = draw_s.value*ypoints + draw_r.value*randpoints + draw_t.value*trendpoints
    smoothpoints = draw_m.value*moving_avg(sumpoints,5)

    # I don't really understand "with", but it seems to work. 
    # This time there are two traces (trace0 and trace1) in the graph, each with x and y values.
    with g.batch_update():
        g.data[0].x = xpoints
        g.data[0].y = sumpoints
        g.data[1].x = xpoints
        g.data[1].y = smoothpoints

# The next few calls I don't really understand. 
# Presumably I have to look up what the "observe" method is for "widget" objects. 
# It seems as if the "observe" method needs two parameters: 1) the function to call and 2) the "names" parameters. 
# `names="value"` seems to be saying: "pass these parameters with their values into the 'response' function". 
# Or something like that.
        
ncycles.observe(response, names="value")
noiselevel.observe(response, names="value")
draw_s.observe(response, names="value")
draw_m.observe(response, names="value")
draw_r.observe(response, names="value")
draw_t.observe(response, names="value")
```

```python
# Finish building the layout, this time an Hbox for two sliders and sliders next to checkboxes
container2 = widgets.VBox([ncycles, noiselevel])
container3 = widgets.HBox([container1, container2])

# Finally, run the dashboard. 
widgets.VBox([container3, g])

# NOTE I don't like how "smoothed" goes to zero when set to "off" but that can be 
# figured out in a subsequent version that uses panda dataframes to manage the various 
# traces instead of independent time series. 
```

### Questions students could consider
These are examples of questions to drive teaching discussions or learning assignments. Questions are not necessarily well-posed. Also, most are judgement calls - which is part of the point!
1. How much noise does it take to obscure the fact that the signal is a nice sinewave?
2. "Smoothing" is a simple "boxcar", or 5-point moving average. How much MORE noise can be managed before the smoothed signal begins to loose its useful character?
3. If there are only 2 or 3 cycles of signal, can you tell there is a trend? What are the implications for the "length" of your data set or series of measurements? 
4. Does noise obscure the fact that there is a superimposed linear trend? 
5. How much data (i.e. how long do you have to take measurments) before the trend is observed? 
6. Does this necessary length for measuring the phenomenon vary if there is more noise? 
7. Pose your own question AND answer it.  

```python
# Next steps are given here as comments instead of markdown so they don't appear in Voila.
#   1. Change so that options are "display data" and "display smoothed" or both. i.e. toggle plots of trace0 and/or trace1. 
#   2. A more "Pythonesque" approach would use Pandas dataframes to contain the signal, noise, trend, result and the smoothed version of result, all in a dataframe who's index is x-axis. 
#
# Sources for figuring out this implementation:
#   Getting Plotly to work in Voila is outlined here: https://github.com/voila-dashboards/voila/issues/284
#   Using plotly figurewidget was guided by https://plotly.com/python/figurewidget-app/
#     However, that page does not re-calculate a time series - it uses widgets to fetch different data from a frame.
#     In fact, that would probably be a better approach - signal, noise, trend, result and smoothed all in a dataframe who's index is x-axis.
#   The "Figure" data structure is detailed in https://plotly.com/python/figure-structure/
#   Layout details are at https://plotly.com/python/reference/layout/, and other details via that page's left menu.
```

```python

```
