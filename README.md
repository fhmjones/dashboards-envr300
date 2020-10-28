# Dashboards, initially for envr300

This repo is accumulating code, data and strategies for interactive exploration of concepts and data sets in envr300 [Introduction to Research in Environmental Science](https://www.eoas.ubc.ca/academics/courses/envr300).

This is also where we are learning to build dashboards using ipywidgets with a plotting library of your choice. Here is the sequence of development:

* We started in the folder "**MonaLoaCO2**" with file "trial04" (trial "05" is same but "cleaner") using `bqplot` for plotting.
* Then we backed off a bit and used `matplotlib` for the more complete "MonaLoaCO2" dashboard in file "co2-ver01".
* Then we started work in the "**ThreeSignals**" folder using the `plotly` library. The first two versions, "plotytest01" and "plotlytest02" are commented, and the third version "plotlytest03" is cleaned up for demonstration as a Voila Dashboard.
* Pointers to libraries used are given in the respective Jupyter Notebooks either as markdown cells or within comments next to code.

For development notes and sources, see comments and documentation in each program's markdown `md` or notebook `ipynb` file.

## MonaLoaCO2

**Goals**: Have students explore the capabilities and limitations of **linear models based on measurements** for explaining or predicting a time-varying physical phenomenon.

This was the first dashboard built, so it was a first exposure to using the `ipywidgets` library for making interactive figures. Files `trial04` and `trial 05` are similar and represent first attempts. See their commented code. `LHeagy's-example` is the unchanged code used for inspiration. The file `co2-ver01` is configured for demonstrating how a dashboard might look and feel for the instructor.

Based on the MonaLoa carbon dioxide data since 1958, this dashboard has three parts. The concept and code are derived from [L. Heagy's presentation](https://ubc-dsci.github.io/jupyterdays/sessions/heagy/widgets-and-dashboards.html) at UBC's Jupyter Days 2020.

1. First, the publically accessible measurments of CO2 in ppm (without blanks) are plotted. User can choose raw or seasonally adjusted data, change plot window length, and adjust the slope and intercept of a line. The goal on this interactive plot is to set the line to model the first 5 years of data, then set a prediction year.
2. Then do the same for the last 5 yrs of data using the _second_ interactive figure.
3. Finally, plot the whole dataset with both linear models and the prediction year values. 

**Current status**: this all works, but could be made "prettier". Commentary in the Voila dashboard may be too long. Conversion to use of plotly library will likely be worth while so that dashboards all use the same plotting environment. This will ensure ease of maintenance, and consistent look and feel for users.

## threesignals

**Goals**: Demonstrate to students how various components can contribute to a complete timeseries signal. Currently, the procedure involves a sine wave, linear trend, random noise and smoothing of the result using a 5-pt moving average. Each can be enabled or disabled. Length of the sinewave can be adjusted from 1 to 10 cycles, and noise level can be adjusted.

**Current status**: This is the first demo to have been made to work within Voila using the `plotly` library's `figure widget` method. We need to discuss what exactly instructors want this dashboard to show and what we can do to make it so students can use it constructively. Next step is probably to make this code work using dataframes rather than individual time series for the various components. 

## Vancouver-Ozone

Not yet a dashboard. Goals so far:

* have students work with "messy" data sets (ozone from sensours in SW British Columbia).
* explore impact of plotting options on interpreability (eg. dots, lines, both, maybe others)
* compare ozone measurements at two locations, one near the ocean, and one inland.
* explore processing necessary to make differences most clearly visible.

**Current status** Plotting using `bqplot` library was explored. This will likely be replaced to use `plotly` library, based on "better" experiences learned with the "threesignals" dashboard.

```python

```
