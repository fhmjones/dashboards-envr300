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


Sources for figuring this out is: 
* see plotytest01 for first attempts. That worked but didn't work in Voila.
* The solution used below is suggested by the page: https://github.com/voila-dashboards/voila/issues/284
* plotly figurewidget was made to run in Voila using guidelines here: https://plotly.com/python/figurewidget-app/
* However, that example does not re-calculate a time series. It uses widgets to fetch different data from a frame. I'll try an approach using dataframes later. 
* Recaluating our time series each time is probably not efficient, but it seems to work.
* Also, the "Figure" data structure is detailed in https://plotly.com/python/figure-structure/
* Layout details are at https://plotly.com/python/reference/layout/, and other details via that page's left menu.

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
# This time we start by defining the widget objects

ncycles = widgets.FloatSlider(
    min=1, max=10, step=0.25, value=2.0, description='Num. cycles'
)

noiselevel = widgets.FloatSlider(
    min=0, max=5, step=0.25, value=1.0, description='Noise'
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

# Begin to define the layout of the dashboard. The Vbox puts three checkboxes in a column. 
container1 = widgets.VBox(children=[draw_s, draw_r, draw_t]) 
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

sumpoints = draw_s.value*ypoints + draw_r.value*randpoints + draw_t.value*trendpoints

# The graph (or 'trace') for the figure will be defined as a scatter plot, of type "lines".
trace1 = go.Scatter(x=xpoints, y=sumpoints, mode="lines")

# Now build the figure and define non-default parameters for this figure
g = go.FigureWidget(data=[trace1], 
                    layout=go.Layout(title=dict(text='Sinewave + trend + noise')))

g.layout.width = 700
g.layout.height = 450
g.layout.xaxis.title = 'x axis'
g.layout.yaxis.title = 'Amplitude'
g.layout.xaxis.range=[0.,11.]
g.layout.yaxis.range=[-4.,8.]
```

```python
# function to handle input from the widgets, and alter the state of the graph

def response(change):   
    xpoints = np.arange(0, ncycles.value, 0.05)
    N=len(xpoints)         #this may not be the most sophisticated approach 
    ypoints = np.sin(xpoints*2*math.pi)
    randpoints = noiselevel.value * (random.rand(N)-.5)
    trendpoints = 0.4*xpoints + 0.5

    sumpoints = draw_s.value*ypoints + draw_r.value*randpoints + draw_t.value*trendpoints
    
    # I don't really understand "with", but it seems to work. 
    # This time there is just one trace in the graph with x and y values.
    with g.batch_update():
        g.data[0].x = xpoints
        g.data[0].y = sumpoints

# The next few calls I don't really understand. 
# Presumably I have to look up what the "observe" method is for "widget" objects. 
# It seems as if the "observe" method needs two parameters: 1) the function to call and 2) the "names" parameters. 
# `names="value"` seems to be saying: "pass these parameters with their values into the 'response' function". 
# Or something like that.

ncycles.observe(response, names="value")
noiselevel.observe(response, names="value")
draw_s.observe(response, names="value")
draw_r.observe(response, names="value")
draw_t.observe(response, names="value")

```

```python
# Finish building the layout, this time an Hbox for the two sliders. 
container2 = widgets.HBox([ncycles, noiselevel])

# Finally, run the dashboard. 
widgets.VBox([container1, container2, g])
```
