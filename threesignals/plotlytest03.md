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


### Purpose
Demonstrate a synthetic signal consisting of "data" + random noise + a linear trend. This is a first attempt. It works but is not likely the most versatile solution. See notes on sources and recommendations at the end of this page. 

Explore the dashboard and its controls. Note the figure controls (above right of the figure) only appear when your mouse is within the figure. 

**Questions to consider:**
These are a few ideas for issues that could drive teaching discussions or learning activities or assignments. They are not necessarily well-posed; just some ideas thrown out there. Most are judgement calls - which is part of the point!
* How much noise does it take to obscure the fact that the signal is a nice sinewave?
* "Smoothing" is a simple "boxcar", or 5-point moving average. How much MORE noise can be managed before the smoothed signal begins to loose its useful character?
* If there are only 2 or 3 cycles of signal, can you tell there is a trend? What are the implications for the "length" of your data set or series of measurements? 
* Does noise obscure the fact that there is a superimposed linear trend? 
* How much data (i.e. how long do you have to take measurments) before the trend is observed? 
* Does this necessary length for measuring the phenomenon vary if there is more noise? 
* Pose your own question AND answer it.  

```python
import plotly
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode(connected = True)

import plotly
import plotly.graph_objs as go
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

container1 = widgets.VBox(children=[draw_s, draw_r, draw_t, draw_m]) 
```

```python
# Discussion on options for moving avg: 
#  https://stackoverflow.com/questions/14313510/how-to-calculate-moving-average-using-numpy
# "convolve" avoids going to pandas dataframes. However, using Pandas is probably better, but 
# Pandas should be used from the start if that's what you want. 

def moving_avg(x, w):
    y = np.convolve(x, np.ones(w), 'valid') / w
    z = np.roll(y, int(w/2))
    #roll wraps end points back to first points, so set these to zero; a cludge, but works for now.
    z[:2] = 0
    return z
```

```python
# Assign an empty figure widget with one trace
# it seems the figure has to be built first, then built again in the widget handling code. 

xpoints = np.arange(0, ncycles.value, 0.05)
N=len(xpoints)         #this may not be the most sophisticated approach 
ypoints = np.sin(xpoints*2*math.pi)
randpoints = noiselevel.value * (random.rand(N)-.5)
trendpoints = 0.4*xpoints + 0.5

sumpoints = draw_s.value*ypoints + draw_r.value*randpoints + draw_t.value*trendpoints
smoothpoints = draw_m.value*moving_avg(sumpoints,5)

trace0 = go.Scatter(x=xpoints, y=sumpoints, mode="lines", name="signal")
trace1 = go.Scatter(x=xpoints, y=smoothpoints, mode="lines", name="smoothed")
g = go.FigureWidget(data=[trace0, trace1], 
                    layout=go.Layout(title=dict(text='Sinewave+trend+noise & 5-point moving average')))
g.layout.width = 700
g.layout.height = 450
```

```python
# function to handle input from the widgets, and alter the state of the graph
# I don't really know how this works, but it looks like the "observe" functions are 
# monitoring the widgets and generating the calls back to the "response" function.

def response(change):   
    xpoints = np.arange(0, ncycles.value, 0.05)
    N=len(xpoints)         #this may not be the most sophisticated approach 
    ypoints = np.sin(xpoints*2*math.pi)
    randpoints = noiselevel.value * (random.rand(N)-.5)
    trendpoints = 0.4*xpoints + 0.5

    sumpoints = draw_s.value*ypoints + draw_r.value*randpoints + draw_t.value*trendpoints
    smoothpoints = draw_m.value*moving_avg(sumpoints,5)
    
    with g.batch_update():
        g.data[0].x = xpoints
        g.data[0].y = sumpoints
        g.data[1].x = xpoints
        g.data[1].y = smoothpoints

ncycles.observe(response, names="value")
noiselevel.observe(response, names="value")
draw_s.observe(response, names="value")
draw_m.observe(response, names="value")
draw_r.observe(response, names="value")
draw_t.observe(response, names="value")

g.layout.xaxis.title = 'x axis'
g.layout.yaxis.title = 'Amplitude'
g.layout.xaxis.range=[0.,11.]
g.layout.yaxis.range=[-4.,8.]
```

```python
# run it
container2 = widgets.HBox([ncycles, noiselevel])
widgets.VBox([container1, container2, g])
```

### Next steps
* modify so options are "display data" and "display smoothed" or both. i.e. toggle plots of trace0 and/or trace1. 
* A more "Pythonesque" approach would use Pandas dataframes to contain the signal, noise, trend, result and the smoothed version of result, all in a dataframe who's index is x-axis. 

### Sources for figuring this out
* see plotlytest01 for first attempts. That worked but didn't work in Voila.
* version plotlytest02 succeeds in the demo without the smoothing option
* this version plotlytest03 adds smoothing. However it is stuck using a two-trace plot, so "no smoothing" means the smoothed trace is shown as zero. I.E. I haven't figured out how to NOT plota one of the traces. 
* Getting Plotly to work in Voila is outlined here: https://github.com/voila-dashboards/voila/issues/284
* Using plotly figurewidget was guided by https://plotly.com/python/figurewidget-app/
  * However, that page does not re-calculate a time series - it uses widgets to fetch different data from a frame.
  * In fact, that would probably be a better approach - signal, noise, trend, result and smoothed all in a dataframe who's index is x-axis.
* The "Figure" data structure is detailed in https://plotly.com/python/figure-structure/
* Layout details are at https://plotly.com/python/reference/layout/, and other details via that page's left menu.

```python

```
