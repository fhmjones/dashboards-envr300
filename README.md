# Dashboards, initially for ENVR 300

This repo is accumulating code, data and strategies for interactive exploration of concepts and data sets in [ENVR 300, Introduction to Research in Environmental Science](https://www.eoas.ubc.ca/academics/courses/envr300).

This is also where we are learning to build dashboards using ipywidgets with a plotting library of your choice. Here is the sequence of development:

* We started in the folder "**MonaLoaCO2**" with file "trial04" (trial "05" is same but "cleaner") using `bqplot` for plotting.
* Then we backed off a bit and used `matplotlib` for the more complete "MonaLoaCO2" dashboard in file "co2-ver01".
* Then we started work in the "**ThreeSignals**" folder using the `plotly` library. The first two versions, "plotytest01" and "plotlytest02" are commented, and the third version "plotlytest03" is cleaned up for demonstration as a Voila Dashboard.
* The "**Vancouver-Ozone**" app was started without dashboards to gain more familiarity with using dataframes. This required adapting large datasets so they are small enough to load quickly. Then a dashboard version was built, first exploring use of the `@interact` decorator approach, then using the same method as the "**ThreeSignals**" app.
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

## ThreeSignals

**Goals**: Demonstrate to students how various components can contribute to a complete timeseries signal. Currently, the procedure involves a sine wave, linear trend, random noise and smoothing of the result using a 5-pt moving average. Each can be enabled or disabled. Length of the sinewave can be adjusted from 1 to 10 cycles, and noise level can be adjusted.

**Current status**: This is the first demo to have been made to work within Voila using the `plotly` library's `figure widget` method. We need to discuss what exactly instructors want this dashboard to show and what we can do to make it so students can use it constructively. Next step is probably to make this code work using dataframes rather than individual time series for the various components. 

## Vancouver-Ozone

Goals are to ...

* Have students work with "messy" data sets using ozone from two sensors in SW British Columbia.
* Compare ozone measurements at two locations, one near the ocean, and one inland.
* Compare raw, 7-day moving average and daily maximum 8-hr average. Which makes differences - or the thing you want to learn from the data - most clearly visible? 
* Explore impact of plotting options on interpreability (eg. dots, lines, both, maybe others) (Not yet done.)

**Current status**: Version 01 (file O3-dashbrd01.md) involved plotting with `plotly` library using "decorator" approach to adding interactive widgets. It is more fully commented with development notes. Version 02 (file O3-dashbrd02.md) uses the same callback approach as "**ThreeSignals**" and has only the necessary comments. Additional surrounding documentation was added to make it useful as a learning or teaching application. Attribution for the idea and source of the data are also included. 

Next step may be to add some options to vary plotting options such as dots vs lines, etc. 

```python

```
