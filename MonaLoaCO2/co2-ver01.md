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

# Exploring linear models for prediction

This dashboard is derived from [L. Heagy's presentation](https://ubc-dsci.github.io/jupyterdays/sessions/heagy/widgets-and-dashboards.html) at UBC's Jupyter Days 2020, which in turn is adapted from the [Intro-Jupyter tutorial from ICESat-2Hackweek](https://github.com/ICESAT-2HackWeek/intro-jupyter), which has contributions from: [Shane Grigsby (@espg)](https://github.com/espg), [Lindsey Heagy (@lheagy)](https://github.com/lheagy), [Yara Mohajerani (@yaramohajerani)](https://github.com/yaramohajerani), and [Fernando Pérez (@fperez)](https://github.com/fperez). 


## Motivating example: CO$_2$ at Mauna Loa

The preamble could be rewritten (based on the original) if this becomes "real". But for now, the point of this notebook is to practice working with dataframes, plots and widgets. 

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from matplotlib import rcParams
rcParams["font.size"] = 14
```

```python
co2_data_source = "./data/monthly_in_situ_co2_mlo.csv"
co2_data_full = pd.read_csv(
    co2_data_source, skiprows=np.arange(0, 56), na_values="-99.99"
)

co2_data_full.columns = [
    "year", "month", "date (int)", "date", "raw co2", "seasonally adjusted",
    "fit", "seasonally adjusted fit", "co2 filled", "seasonally adjusted filled" 
]

# for handling NaN's see https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html
co2_data = co2_data_full.dropna()
# co2_data_full
# co2_data
```

```python
# A function to fetch data between year_min and year_max  

def get_data_between(data=co2_data, date_range=None , data_type="seasonally adjusted"):    
    if date_range is None:
        date_range = data["date"].min(), data["date"].max()

    # find the data between the minimimum and maximum years
    indices = (data["date"] >= date_range[0]) & (data["date"] <= date_range[1]) 
    return data["date"][indices], data[data_type][indices]
```

```python
# A function to plot data between year_min and year_max

def plot_co2_data(data=co2_data, date_range=None, data_type="seasonally adjusted", ax=None):
    
    # create a figure if one isn't supplied
    # this approach is explained https://stackoverflow.com/questions/43482191/matplotlib-axes-plot-vs-pyplot-plot
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(8, 5))
        
    dates, data_between = get_data_between(data, date_range, data_type)
    
    # plot data
    ax.plot(dates, data_between, '.',  ms=8)
    ax.grid()
    ax.set_xlabel(f"Year")
    ax.set_ylabel(f"CO$_2$ [ppm]")
    ax.set_title(f"Data type: " + data_type)

    return ax
```

```python
# plot_co2_data(co2_data);
# plot_co2_data(co2_data ,[1958, 1963]);

# not clear what the ';' is doing here - seems to prevent printing return value to stdout.
```

---

### Part 1: Predicting CO$_2$ based on linear fit to the first 5 years of data.

```python
import ipywidgets as widgets
```

```python
# Function to add a line to a plot

def add_line(dates, slope, intercept, ax=None, label=None):
    # create a figure if one isn't supplied
    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    
    y = slope * (dates - np.min(dates)) + intercept
    ax.plot(dates, y, label=label)
```

```python
# A linear model with slope and intercept to predict CO2
def predict_co2(slope, intercept, initial_date, prediction_date):
    a = slope * (prediction_date-initial_date) + intercept
    
    return a
```

```python
# Function for interactivity: it creates a plot with data and the "added" line.
# order of parameters is the order desired in the interactive cell. 
predicted_co2_early = 0
predicted_co2_recent = 0

def plot_fit_co2_data(year_max=2020, slope=1, intercept=300, year_min=1958, predn_yr=2030, data_type="seasonally adjusted", which_pred="early"):
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    plot_co2_data(co2_data, [year_min, year_max], data_type, ax=ax)    
    add_line(np.r_[year_min, year_max], slope, intercept, ax=ax)
    global predicted_co2_early
    global predicted_co2_recent
    co2_value = predict_co2(slope, intercept, year_min, predn_yr)
    if which_pred=="early": 
        predicted_co2_early = co2_value
    else: predicted_co2_recent = co2_value
    predicted_co2_recent
    print(f"Predicted CO2 for {predn_yr}: {co2_value:1.2f} ppm.")
    return ax

# I don't understand "np.r_"
```

#### Step 1, approximate a line to fit the first 5 yrs of data (1958-1963)
* Make sure "**year_max**" is 1963 (5 yrs after the first measurements).
* Adjust "**slope**" and "**intercept**" sliders to make the orange line fit the displayed data points as close as you can. 

#### Step 2, use this linear model to predict CO$_2$ ppm at any given year
* Adjust the "**predn_yr**" slider to choose a year for which you want a predicted CO$_2$; note the value given on the line between sliders and graph.

#### Check this makes sense
* Adjust the graph using slider "**year_max**" so you can see the value predicted by this linear model at the date you chose.

```python
# Interactive method to attach parameter sliders to the figure and present all. 
series = "seasonally adjusted"
year_min_early = 1958
year_max_early = 1963

# "interactive" requires the function & parameters required by that function
w_co2_early = widgets.interactive(
    plot_fit_co2_data,
    slope=widgets.FloatSlider(
        min=0, max=5, step=0.1, value=2
    ),
    intercept=widgets.FloatSlider(
        min=round(co2_data[series].min(),0)-5,
        max=co2_data[series].min()+5, 
        step=0.25,
    ),    
    year_min=widgets.fixed(year_min_early),
    year_max=widgets.FloatSlider(
        min=1950, max=2030, step=1, value=1963
    ),
    predn_yr=widgets.FloatSlider(
        min=1950, max=2030, step=5, value=1965
    ),
    data_type=widgets.RadioButtons(
        options=['seasonally adjusted', 'raw co2'],
        description='Data',
        disabled=False
    ),
    which_pred=widgets.fixed("early")
)
w_co2_early
```

---
### Part 2: Predicting from the most recent 5 years of data.

**Question:** If the trend between 2015 and 2020 continues, what would we expect the CO$_2$ concentration to be in January, 2030? 

Use sliders to explore this "recent" end of the data set. 

```python
series = "seasonally adjusted"
year_min_recent = 2015
year_max_recent = 2020

w_co2_recent = widgets.interactive(
    plot_fit_co2_data, 
    slope=widgets.FloatSlider(
        min=0, max=5, step=0.1, value=2
    ),
    intercept=widgets.FloatSlider(
        min=round(co2_data["seasonally adjusted"].max(),0)-20, 
        max=co2_data["seasonally adjusted"].max(), 
        step=0.25
    ),
    year_min=widgets.FloatSlider(
        min=1950, max=2030, step=1, value=year_min_recent,
    ),
    year_max=widgets.fixed(year_max_recent),
    predn_yr=widgets.FloatSlider(
        min=1950, max=2030, step=5, value=2020
    ),
    data_type=widgets.RadioButtons(
        options=['seasonally adjusted', 'raw co2'],
        description='Data',
        disabled=False
    ),
    which_pred=widgets.fixed("recent")
)
w_co2_recent
```

---

### Part 3: Compare predictions from "recent" and "early" data sets.

**Question:** _Before looking at the next plot(!) ..._ Why are these estimates so different? 

Now compare the slopes and predicted values on one graph 
* Click the "Run Interact" button once. 
* **Do prediction points align with linear models?**
* If NOT set "predn_yr" sliders for both models above to 2030 and click "Run Interact" again. 

```python
from ipywidgets import interact_manual

def plot_predictions(xlim=None, ylim=None, predn_yr=2030):
    ax = plot_co2_data()

    # add predictions
    add_line(
        co2_data["date"], w_co2_early.kwargs["slope"], 
        w_co2_early.kwargs["intercept"],
        label = f"{year_min_early} - {year_max_early} prediction", ax=ax
    )

    add_line(
        co2_data["date"], w_co2_recent.kwargs["slope"], 
# adjust the intercept to use 1958
        w_co2_recent.kwargs["intercept"] - (year_min_recent-co2_data["date"].min())*w_co2_recent.kwargs["slope"], 
        label = f"{year_min_recent} - {year_max_recent} prediction", ax=ax
    ) 

    # add our predictions 
    ax.plot(predn_yr, predicted_co2_early, 'C1o')
    ax.text(
        predn_yr - 1, predicted_co2_early, 
        f"{predicted_co2_early:1.2f} ppm", ha="right", va="center"
    )

    ax.plot(predn_yr, predicted_co2_recent, 'C2o')
    ax.text(
        predn_yr - 1, predicted_co2_recent, 
        f"{predicted_co2_recent:1.2f} ppm", ha="right", va="center"
    )
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
# plot_predictions()

im = interact_manual(
    plot_predictions, 
    xlim=widgets.fixed(None), 
    ylim=widgets.fixed(None), 
    predn_yr=widgets.fixed(2030)
);
```

```python

```

---
### Discussion:

Within small enough regions, the data follow an approximately linear trend, so a linear model has some predictive power. To consider these questions, revisit the two "early" and "recent" interactive plots above.
1. Out to which year would you trust the model built with the data from 1958 - 1963? 
2. Where does it start to break down?
3. How far out would you trust our predictions with data from 2015 - 2020? Would you trust our model to predict CO$_2$ in the year 2050? 
4. How might you approach building a model to fit all of our data? 


