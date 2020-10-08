---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.4.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Learning Python, with a purpose

## Moving average on Mona Loa CO2 data 

What moving average window length provides the result with least influence of diurnal contribution?

NOTE - adapt LH's version from [here](https://ubc-dsci.github.io/jupyterdays/sessions/heagy/widgets-and-dashboards.html).

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bqplot.pyplot as bqplt
```

```python
# Fetch data from the CSV file. Plot to examin.
df = pd.read_csv(".\data\co2_mm_mlo.csv", header=70)
df.columns = ['yr','mth','dec_date','avg','interp','trend','ndays']
#df.head(30)
```

```python
#First make avg_cl = series of original averages, 
s = df['avg']

# I don't know why this has to be done. Something to do with a SettingWithCopy warning.
avg_cl = s.copy()
#avg_cl[:5], s[:5]
```

```python
# replace negative values with NaN.
n = 0
for x in avg_cl[:]:
    if x < 0:
        avg_cl[n] = np.nan
    n += 1

# Replace NaN with average of adjacent.
# NOTE: fails with adjacent NaN's.
n = 0
for x in avg_cl[:]:
    if np.isnan(x):
        avg_cl[n] = (avg_cl[n-1]+avg_cl[n+1])/2
    n += 1
    
# avg_cl[0:10]
```

* Use the slider to set the **moving average window size** in units of samples (one sample per month).
* Click `Run Interact` to see the raw data (blue) and smoothed result (red).
* Pan or zoom the graph by clicking the **left** "crossed-arrows" button. **Middle** button "Resets" the figure. Use the **right** button to save an image file. 
* Change window size, and re-click `Run Interact` to see changes.

```python
# to make slider work, see https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html
# more hints on building UI at https://ipython-books.github.io/33-mastering-widgets-in-the-jupyter-notebook/

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

# Moving average implemented as convoltion with a box of length "window".
# Blanks occure when ever there are NaN's in the calculation.

date = df["dec_date"]

def smooth(window):    
    filter = np.repeat(1,window)/window
    smoothed = np.convolve(avg_cl,filter,'valid')

    # what decimal_date corresponds to each convolved (i.e. filtered) value?
    first_sm_date_index = len(date)-len(smoothed)-int(window/2)

    # display with interactive plot
    bqplt.clear()
    bqplt.figure(title='Raw CO2 (blue), and smoothed (red) with' + str(window) + "-point window.")
    bqplt.plot(date, avg_cl, 'b-')
    bqplt.plot(date[first_sm_date_index:], smoothed, 'r-')
    bqplt.show()

# generate the user interface. 
# for 'interact_manual' see https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html
im = interact_manual(smooth, window=widgets.IntSlider(min=1, max=19, step=2, value=7));
```

Moving average implemented as convoltion with a box of length "window".
Derived from source found [here](https://gordoncluster.wordpress.com/2014/02/13/python-numpy-how-to-generate-moving-averages-efficiently-part-2/).  Look up `np.convolve` for built-in convolution function. NOTE this simple box-car may not be the best choice but the goal at this stage is to work out the sequence, not compute the optimal smoothed version of this particular data set. 
