# Dashboards for envr300

Code and data for interactive exploration of concepts and data sets in envr300 [Introduction to Research in Environmental Science](https://www.eoas.ubc.ca/academics/courses/envr300).

For sources and development notes, see comments and documentation in each program's markdown `md` or notebook `ipynb` file.

## MonaLoaCO2

Based on the MonaLoa carbon dioxide data since 1958, this dashboard has three parts. Current (Oct 7th) version is co2-ver01.

1. The publically accessible measurments of CO2 in ppm (without blanks) are plotted. User can choose raw or seasonally adjusted data, change plot window length, and adjust the slope and intercept of a line. Goal is to set the line to model the first 5 years of data, then set a prediction year.
2. Do the same for the last 5 yrs of data. 
3. Based on prediction year selected above, plot the whole dataset with both linear models and the prediction year values.

**Current status**: this all works, but could be made "prettier". Commentary in the Voila dashboard may be too long. Conversion to use of plotly library will likely be worth while so that dashboards all use the same plotting environment. This will ensure ease of maintenance, and consistent look and feel for users.

## Vancouver-Ozone

Not yet a dashboard. Goals so far:

* Work with "messy" data sets (ozone from sensours in SW British Columbia).
* explore impact of plotting options on interpreability (eg. dots, lines, both, maybe others)
* compare ozone measurements at two locations, one near the ocean, and one inland.
* explore processing necessary to make differences most clearly visible.

**Current status** (Oct 7): plotting using `bqplot` library was explored. This will likely be replaced to use plotly library, based on "better" experiences learned with the "threesignals" dashboard.

## threesignals 

Goals: Demonstrate various contributors to a complete signal. Currently, the procedure involves a sine wave, linear trend and random noise. Each can be enabled or disabled. Length of the sinewave can be adjusted from 1 to 10 cycles.

**Current status**: as of Oct 7th this is the first demo to have been made to work within Voila using the `plotly` library's "figure widget" method. We need to discuss what exactly instructors want this dashboard to show andwhat we can do to make so students can use it constructively.

