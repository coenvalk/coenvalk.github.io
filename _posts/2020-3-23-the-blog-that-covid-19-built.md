---
layout: post
title:  The Blog that COVID-19 Built
date:   2020-03-23
categories: technology
---

# COVID-19 Exploration

# Introduction

## Related Reading

- An excellent [article](https://www.washingtonpost.com/graphics/2020/world/corona-simulator/) from the Washington Post that shows how social distancing can make a difference in a large-scale pandemic.
- John Hopkins University [articles and whitepapers](https://systems.jhu.edu/research/public-health/ncov/) modeling the spread of the virus.
- [Article](http://orgnet.com/TNA.pdf) suggesting the spread of infectious disease follows a power law as opposed to a exponential growth.

## Data

This time series data is updated daily by Johns Hopkins University. It records the number of confirmed, recovered, and dead cases in each country / region per day. Let's view what the data looks like right now:


```python
import os
import numpy as np
import pandas as pd
from scipy import optimize as opt
from matplotlib import pyplot as plt
```


```python
data_root = "COVID-19/csse_covid_19_data/csse_covid_19_time_series/"

confirmed_df = pd.read_csv(os.path.join(data_root, "time_series_19-covid-Confirmed.csv"), index_col=['Country/Region', 'Province/State', 'Lat', 'Long'])
deaths_df = pd.read_csv(os.path.join(data_root, "time_series_19-covid-Deaths.csv"), index_col=['Country/Region', 'Province/State', 'Lat', 'Long'])
recovered_df = pd.read_csv(os.path.join(data_root, "time_series_19-covid-Recovered.csv"), index_col=['Country/Region', 'Province/State', 'Lat', 'Long'])
```


```python
"""
country = "US"

confirmed_df = confirmed_df.loc[country]
deaths_df = deaths_df.loc[country]
recovered_df = recovered_df.loc[country]
"""
```




    '\ncountry = "US"\n\nconfirmed_df = confirmed_df.loc[country]\ndeaths_df = deaths_df.loc[country]\nrecovered_df = recovered_df.loc[country]\n'




```python
global_confirmed = confirmed_df.sum()
global_deaths = deaths_df.sum()
global_recovered = recovered_df.sum()
```


```python
global_confirmed.plot(title="Global Confirmed Cases")
```




    <matplotlib.axes._subplots.AxesSubplot at 0x20fcd6ba160>




![png](/assets/images/output_5_1.png)



```python
total_df = pd.DataFrame({
    "Deaths": global_deaths,
    "Confirmed": global_confirmed,
    "Recovered": global_recovered
})


N = total_df.sum(axis=1)
total_df['Healthy'] = N.max() - N

total_df[['Deaths', 'Confirmed', 'Healthy', 'Recovered']].plot.area(title="Global Case State Over Time", colormap="RdYlGn")
plt.show()

total_df[['Deaths', 'Confirmed', 'Recovered']].iloc[-1].plot.pie(title="Case Breakdown", colormap="RdYlGn")
plt.show()
```


![png](/assets/images/output_6_0.png)



![png](/assets/images/output_6_1.png)



```python
def f(x, c, k, x0, y0):
    return c / (1 + np.exp(-k*(x-x0))) + y0
```


```python
# make data:
last_days = 14
x = np.arange(1, len(global_confirmed) + 1)[-last_days:]
y = global_confirmed.values[-last_days:]
```


```python
plt.plot(x, y, 'o')
plt.xlabel('Time')
plt.ylabel('# Cases')
plt.xscale('log')
plt.yscale('log')
plt.title('Number of Cases Over Time')
plt.show()
```


![png](/assets/images/output_9_0.png)



{% highlight py %}
x_log = np.log(x)
y_log = np.log(y)
m, b = np.polyfit(x_log, np.log(y), 1)
{% endhighlight %}


```python
x = np.arange(1, len(global_confirmed) + 1)
y = global_confirmed.values
x_log = np.log(x)
y_log = np.log(y)

y_fit_log = m * x_log + b
y_fit = np.exp(y_fit_log)
plt.plot(x, y_fit)
plt.plot(x, y, 'o')
plt.legend(['Best Fit Line', 'Data'])
plt.title("Log Log Cases")
plt.show()
```


![png](/assets/images/output_11_0.png)



```python

```
