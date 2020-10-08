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

## To see if plotly can be used for plotting in dashboards.


Source for figuring this out is: 
* see plotytest01 for first attempts. That worked but didn't work in Voila.
* This page suggests the solution used below: https://github.com/voila-dashboards/voila/issues/284
* making this using plotly figurewidget so it runs in Voila was guided by https://plotly.com/python/figurewidget-app/
* However, that does not re-calculate a time series it uses widgets to fetch different data from a frame. 
* Recaluating our time series might not be as efficient in this code, but it seems to work. 
* also, the "Figure" data structure is detailed in https://plotly.com/python/figure-structure/

```python
from plotly.offline import init_notebook_mode
init_notebook_mode(connected = True)
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

First assign the widgets.

```python
ncycles = widgets.FloatSlider(
    min=1, max=10, step=0.1, value=2.0, description='Num. cycles'
)

draw_s = widgets.Checkbox(
    value=True,
    description='Sine wave',
    disabled=False,
    indent=True
)

draw_r = widgets.Checkbox(
    value=True,
    description='Random noise',
    disabled=False,
    indent=True
)

draw_t = widgets.Checkbox(
    value=True,
    description='Trend line',
    disabled=False,
    indent=True
) 

container1 = widgets.VBox(children=[draw_s, draw_r, draw_t]) 
```

```python
# Assign an empty figure widget with one trace
# it seems the trace has to be built first, then built again in the widget handling code. 

xpoints = np.arange(0, math.pi*ncycles.value*2, 0.05)
N=len(xpoints)         #this may not be the most sophisticated approach 
ypoints = np.sin(xpoints)
randpoints = random.rand(N)
trendpoints = 0.2*xpoints + 0.5

sumpoints = draw_s.value*ypoints + draw_r.value*randpoints + draw_t.value*trendpoints

trace1 = go.Scatter(x=xpoints, y=sumpoints, mode="lines")
g = go.FigureWidget(data=[trace1], 
                    layout=go.Layout(title=dict(text='Sine wave only?')))


```

```python
# function to handle input from the widgets, and alter the state of the graph

def response(change):   
    xpoints = np.arange(0, math.pi*ncycles.value*2, 0.05)
    N=len(xpoints)         #this may not be the most sophisticated approach 
    ypoints = np.sin(xpoints)
    randpoints = random.rand(N)
    trendpoints = 0.2*xpoints + 0.5

    sumpoints = draw_s.value*ypoints + draw_r.value*randpoints + draw_t.value*trendpoints
    
    with g.batch_update():
        g.data[0].x = xpoints
        g.data[0].y = sumpoints
        g.layout.xaxis.title = 'x axis'
        g.layout.yaxis.title = 'y axis'

ncycles.observe(response, names="value")
draw_s.observe(response, names="value")
draw_r.observe(response, names="value")
draw_t.observe(response, names="value")
```

```python
# run it
container2 = widgets.HBox([ncycles])
widgets.VBox([container1,
              container2,
              g])
```

## next steps
* lock the axis so it doesn't auto-fit every time
* adjust noise amplitude? 
* others? 
