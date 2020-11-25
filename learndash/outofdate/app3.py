# -*- coding: utf-8 -*-

# Run this app with `python app3.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# based on ideas in tutorial at https://dash.plotly.com/layout 
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np
from numpy import random
import math #needed for definition of pi

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# make a noisy sine wave on a linear trend
# build the X-axis first, then the three time series: 
ncycles = 10
noiselevel = 1   # value between 0 and, say, 5
xpoints = np.arange(0, ncycles, 0.05)
N=len(xpoints)   # this may not be the most sophisticated approach 
ypoints = np.sin(xpoints*2*math.pi)
randpoints = noiselevel * (random.rand(N)-.5)
trendpoints = 0.4*xpoints + 0.5

# Turn components on or off by multiplying by the binary values returned by check box widgets: "component.value". 
sumpoints = ypoints + randpoints + trendpoints

# make a scatter or line chart of this sine wave
# fig = px.scatter(x=xpoints, y=sumpoints)
fig = px.line(x=xpoints, y=sumpoints, labels={'x':'t', 'y':'sin(t)'})

app.layout = html.Div(children=[
    html.H2(children='Noisy sine wave on a linear trend'),

    html.Div(children='''
        A dashboard to explore signals and noise.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)