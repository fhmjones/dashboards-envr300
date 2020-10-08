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

## Fourth prgm: convert to use dataframes

Recall, to start in this repo's folder, the "numeric" environment needs setting, then the notebook environment is started with jupyter notebook.

```
conda activate numeric
jupyter notebook
```

Interactive plot using widgets from [https://jupyter.org/widgets](https://jupyter.org/widgets)

* Installation with conda: `conda install -c conda-forge bqplot`
* Then to install Voila, see Voila GitHub repo's [readme.md file](https://github.com/voila-dashboards/voila/blob/master/README.md): `conda install -c conda-forge voila`
* Run the code with Voila defaults: `voila test03.ipynb`

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
#df
```

```python
#plt.plot(df["avg"])
#df.isnull() 
#avg_cl = df['avg']
#plt.plot(avg_cl)
```

```python
#First make avg_cl = series of original averages, 
s = df['avg']

# I don't know why this has to be done. Something to do with a SettingWithCopy warning.
avg_cl = s.copy()
#avg_cl[:5], s[:5]
```

```python
# In general, values that are less than zero are 'NaN'
# Since there will be smoothing, there should be no NaN's.
# Otherwise there will be long segments that can not be smoothed.
# However, with this data set, the "interp" column can be used directly since it fills in the NaNs 

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

# raises warnings about trying to set values on a copy of a slice from a dataframe.
# documentation - https://pandas.pydata.org/pandas-docs/stable/getting_started/10min.html
```

```python
#plt.plot(avg_cl)
```

Moving average implemented as convoltion with a box of length "window".
Derived from source found [here](https://gordoncluster.wordpress.com/2014/02/13/python-numpy-how-to-generate-moving-averages-efficiently-part-2/).  Look up `np.convolve` for built-in convolution function. NOTE this simple box-car may not be the best choice but this goal here is to work out the sequence, not compute the optimal smoothed version of this particular data set. 

**NOTE**: Within the interactive display, avoid scolling the page when zooming (mouse wheel) by pressing "shift" while rolling the wheel.

For plot line color, type, and other parameters, see [Matplotlib docs](https://matplotlib.org/2.1.1/api/_as_gen/matplotlib.pyplot.plot.html).

```python
# to make slider work, see https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html
# more hints on building UI at https://ipython-books.github.io/33-mastering-widgets-in-the-jupyter-notebook/

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

# Moving average implemented as convoltion with a box of length "window".
# Blanks occure wherever there are NaN's in the calculation.

date = df["dec_date"]
def smooth(window):    
    filter = np.repeat(1,window)/window
    smoothed = np.convolve(avg_cl,filter,'valid')

    # what decimal_date corresponds to each convolved (i.e. filtered) value?
    first_sm_date_index = len(date)-len(smoothed)-int(window/2)

    # display with interactive plot
    bqplt.clear()
    bqplt.figure(title='Raw CO2, and smoothed with ' + str(window) + "-point window.")
    bqplt.plot(date, avg_cl)
    bqplt.plot(date[first_sm_date_index:], smoothed, 'r-')
    bqplt.show()

# generate the user interface. 
# for 'interact_manual' see https://ipywidgets.readthedocs.io/en/latest/examples/Using%20Interact.html
im = interact_manual(smooth, window=widgets.IntSlider(min=1, max=49, step=1, value=11));
```

To see this without code cells, run via Voila using defaults: `voila test03.ipynb`. Or the "Voila" button on the toolbar.

**Next**:

1. solve the adjacent NaN problem.
2. fetch data from specified location - file and URL - rather than hard-coded CSV file.

```python

```
