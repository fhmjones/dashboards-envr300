# Exploring linear models for prediction
# -*- coding: utf-8 -*-

# Run this app with `python app3.py` and
# visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/ 

# based on ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
# plotly express could be used for simple applications
# but this app needs to build plotly graph components separately 
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

##################################
# Fetch and prep the data
# read in the data from the prepared CSV file. 
co2_data_source = "./data/monthly_in_situ_co2_mlo.csv"
co2_data_full = pd.read_csv(
    co2_data_source, skiprows=np.arange(0, 56), na_values="-99.99"
)

co2_data_full.columns = [
    "year", "month", "date_int", "date", "raw_co2", "seasonally_adjusted",
    "fit", "seasonally_adjusted_fit", "co2 filled", "seasonally_adjusted_filled" 
]

# for handling NaN's see https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
co2_data = co2_data_full.dropna()

##################################
# Lay out the page 
app.layout = html.Div([
# Introduction
    dcc.Markdown('''
        ### Approximate linear models for CO2 at MonaLoa, Hawaii

        #### Purpose: 

        Fit lines to first 5 years of data, then again to most recent 5 years of data. 
        Do these two linear approximations to the process predict the same result? 
        
        '''),
    # controls for plot
    html.Div([
        dcc.Markdown(''' _Slope:_ '''),
        dcc.Slider(
            id='line_slope', min=0, max=3, step=0.1, value=2,
            marks={0:'0', 1:'1', 2:'2', 3:'3'},
            tooltip={'always_visible':True, 'placement':'topLeft'}
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Markdown(''' _Intercept:_ '''),
        dcc.Slider(
            id='line_intcpt', min=310, max=320, step=0.25,value=312,
            marks={310:'310', 312:'312', 314:'314', 316:'316', 318:'318', 320:'320'},
            tooltip={'always_visible':True, 'placement':'topLeft'}
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        dcc.Markdown(''' _Signal type:_ '''),
         dcc.RadioItems(
            id='Data_type',
            options=[
            {'label': 'Adjusted', 'value': 'adj'},
            {'label': 'Raw', 'value': 'raw'}
            ],
            value='adj'
        ),
    ], style={'width': '90%', 'text-align':'center', 'display': 'inline-block'}),

# after controls, place plot
    dcc.Graph(id='graph'),

# closing text
    dcc.Markdown('''
    -------

    ### Discussion

    Within small enough regions, the data follow an approximately linear trend, so a linear model has some predictive power. To consider these questions, revisit the two "early" and "recent" interactive plots above.
    
    1. Out to which year would you trust the model built with the data from 1958 - 1963? 
    2. Where does it start to break down?
    3. How far out would you trust our predictions with data from 2015 - 2020? Would you trust our model to predict CO$_2$ in the year 2050? 
    4. How might you approach building a model to fit all of our data? 

    ### Attribution
    
    Derived from [L. Heagy's presentation](https://ubc-dsci.github.io/jupyterdays/sessions/heagy/widgets-and-dashboards.html) at UBC's Jupyter Days 2020, which in turn is adapted from the [Intro-Jupyter tutorial from ICESat-2Hackweek](https://github.com/ICESAT-2HackWeek/intro-jupyter), which has contributions from: [Shane Grigsby (@espg)](https://github.com/espg), [Lindsey Heagy (@lheagy)](https://github.com/lheagy), 
    [Yara Mohajerani (@yaramohajerani)](https://github.com/yaramohajerani), 
    and [Fernando Pérez (@fperez)](https://github.com/fperez). 
    Adaptation code by F. Jones.
    
    '''),
], style={'width': '900px'}
)

# end of layout and definition of controls.
##################################
# The callback function with it's app.callback wrapper.
@app.callback(
    Output('graph', 'figure'),
    Input('line_slope', 'value'),
    Input('line_intcpt', 'value'),
    Input('Data_type', 'value'),
    )
def update_graph(line_slope, line_intcpt, Data_type):
# construct all the figure's components
    plot = go.Figure()

    l1 = line_slope * (co2_data.date - np.min(co2_data.date)) + line_intcpt

    if Data_type == 'raw':
        plot.add_trace(go.Scatter(x=co2_data.date, y=co2_data.raw_co2, mode='markers',
            line=dict(color='MediumTurquoise'), name="CO2"))
    if Data_type == 'adj':
        plot.add_trace(go.Scatter(x=co2_data.date, y=co2_data.seasonally_adjusted, mode='markers',
            line=dict(color='MediumTurquoise'), name="CO2"))
    
    plot.add_trace(go.Scatter(x=co2_data.date, y=l1, mode='lines',
        line=dict(color='SandyBrown'), name="linear fit"))
    
    plot.layout.title = "CO2 ppm"

    plot.update_layout(xaxis_title='Time', yaxis_title='ppm')
    plot.update_xaxes(range=[1958, 1963])
    plot.update_yaxes(range=[310, 325])

    return plot

if __name__ == '__main__':
    app.run_server(debug=True)