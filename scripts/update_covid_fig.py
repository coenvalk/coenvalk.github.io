import os
import numpy as np
import pandas as pd
from git import Repo
from matplotlib import pyplot as plt

repo_path = "../"
data_root = "./COVID-19/csse_covid_19_data/csse_covid_19_time_series/"
output_path = "../assets/images/"

repo = Repo(repo_path)

for submodule in repo.submodules:
    submodule.update(init=True, to_latest_revision=True)

confirmed_df = pd.read_csv(os.path.join(data_root, "time_series_19-covid-Confirmed.csv"), index_col=['Country/Region', 'Province/State', 'Lat', 'Long'])
deaths_df = pd.read_csv(os.path.join(data_root, "time_series_19-covid-Deaths.csv"), index_col=['Country/Region', 'Province/State', 'Lat', 'Long'])
recovered_df = pd.read_csv(os.path.join(data_root, "time_series_19-covid-Recovered.csv"), index_col=['Country/Region', 'Province/State', 'Lat', 'Long'])

global_confirmed = confirmed_df.sum()
global_deaths = deaths_df.sum()
global_recovered = recovered_df.sum()

total_df = pd.DataFrame({
    "Deaths": global_deaths,
    "Confirmed": global_confirmed,
    "Recovered": global_recovered
})

N = total_df.sum(axis=1)
total_df['Healthy'] = N.max() - N

x = np.arange(1, len(total_df) + 1)
y = global_confirmed.values
x_log = np.log(x)
y_log = np.log(y)

m, b = np.polyfit(x_log, y_log, 1)

y_fit_log = m * x_log + b
y_fit = np.exp(y_fit_log)

plt.plot(x, total_df["Confirmed"], 'o')
plt.plot(x, y_fit)
plt.title("Global Active Cases")
plt.xlabel("Time")
plt.ylabel("# Confirmed Cases")
plt.legend(["Raw Data", "Best Fit Line"])
plt.xscale("log")
plt.yscale("log")
plt.savefig(os.path.join(output_path, "COVID-19_confirmed.png"))

total_df[['Deaths', 'Confirmed', 'Healthy', 'Recovered']].plot.area(title="Global Case Breakdown Over Time", colormap="RdYlGn")
plt.savefig(os.path.join(output_path, "COVID-19.png"))
