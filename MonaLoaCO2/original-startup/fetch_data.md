```python
"""
download the Mauna Loa CO2 data as a csv file and plot it
"""
import urllib.request
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
```

```python
#
# use antialiased driver for batch printing (no window popup)
#
matplotlib.use('Agg')
root_url = "ftp://aftp.cmdl.noaa.gov/products/trends/co2"
filename = "co2_weekly_mlo.csv"
#filename = "co2_mm_mlo.csv"
url = f"{root_url}/{filename}"
filename, extra =urllib.request.urlretrieve(url, filename)
print(f"retrieved file: {filename}\n\ncommand output is:\n {extra}\n")
#
# read the file into a pandas data frame, skipping comments
#
the_df = pd.read_csv(filename,comment="#")
co2 = the_df["average"].to_numpy()
week = the_df["decimal"].to_numpy()
#
# filter out missing values
#
co2[co2 < 0] = np.nan
print(the_df.head())
fig,ax = plt.subplots(1,1,figsize=(10,10))
ax.grid(True)
ax.plot(week, co2)
fig.savefig("co2_fig.png")
```

```python

```
