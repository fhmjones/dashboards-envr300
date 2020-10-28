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
* plotly plot at https://www.tutorialspoint.com/plotly/plotly_plotting_inline_with_jupyter_notebook.htm
* random via https://www.w3schools.com/python/numpy_random.asp. Note that importing `random` from `numpy` seems necessary. 
* array length using Python length function from https://www.w3schools.com/python/ref_func_len.asp. 

**Note:** this works in Jupyter notebook but not in Voila. Apparently you have to use Plotly figure widgets. It's not good enough to just plot the figure. See https://github.com/voila-dashboards/voila/issues/284.

The next step is to convert to figure widgets. See "plotlytest02". 

```python
import plotly
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode
init_notebook_mode(connected = True)
import numpy as np
from numpy import random
import math #needed for definition of pi
import ipywidgets as widgets
```

```python
# Work is done in a function which `widgets.interactive` will call to make it interactive.
# Parameters for this function are set by `widgets.interactive` (next cell).

def plot_signal(ncycles=1.0, draw_s=True, draw_r=True, draw_t=True):
    xpoints = np.arange(0, math.pi*ncycles*2, 0.05)
    N=len(xpoints)         #this may not be the most sophisticated approach 
    ypoints = np.sin(xpoints)
    randpoints = random.rand(N)
    trendpoints = 0.2*xpoints + 0.5

    sumpoints = draw_s*ypoints + draw_r*randpoints + draw_t*trendpoints

    trace0 = go.Scatter(
       x = xpoints, y = sumpoints
    )
    data = [trace0]
    plotly.offline.iplot({ "data": data,"layout": go.Layout(title="Noisy sine wave with linear trend")})
    return()
                
# plot_signal(3.0)
```

```python
# widgets.interactive's first parameter is the function to call (defined above, "plot_signal" in this case), 
# then remaining parameters are the parameters for that function.
# All parameters are widgets in this case, but if preferred, any parameter could be fixed. 

noisy_sine = widgets.interactive(
    plot_signal,
    ncycles = widgets.FloatSlider(
        min=1, max=10, step=0.1, value=2, description='Num. cycles'
    ),
    draw_s = widgets.Checkbox(
        value=True,
        description='Sine wave',
        disabled=False,
        indent=True
    ),
    draw_r = widgets.Checkbox(
        value=True,
        description='Random noise',
        disabled=False,
        indent=True
    ),
    draw_t = widgets.Checkbox(
        value=True,
        description='Trend line',
        disabled=False,
        indent=True
    )
)
noisy_sine
```

**Note**: this works in Jupyter notebook but not in Voila. Apparently you have to use Plotly figure widgets. It's not good enough to just plot the figure. See https://github.com/voila-dashboards/voila/issues/284.

The next step is to convert to figure widgets. See "plotlytest02". 
