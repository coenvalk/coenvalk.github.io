import os
import glob
import numpy as np
import pandas as pd
from git import Repo
from matplotlib import pyplot as plt

repo_path = "../"
data_root = "./COVID-19/csse_covid_19_data/csse_covid_19_time_series/"
output_path = "../assets/images/"

repo = Repo(repo_path)
output = repo.git.submodule('update', '--remote')

confirmed = pd.read_csv(os.path.join(data_root, "time_series_covid19_confirmed_global.csv"))
deaths = pd.read_csv(os.path.join(data_root, "time_series_covid19_deaths_global.csv"))
recovered = pd.read_csv(os.path.join(data_root, "time_series_covid19_recovered_global.csv"))

confirmed = confirmed.drop(columns=["Province/State", "Country/Region", "Lat", "Long"])
deaths = deaths.drop(columns=["Province/State", "Country/Region", "Lat", "Long"])
recovered = recovered.drop(columns=["Province/State", "Country/Region", "Lat", "Long"])

confirmed = confirmed.sum()
deaths = deaths.sum()
recovered = recovered.sum()

total_df = pd.DataFrame({
    "Deaths": deaths,
    "Active": confirmed - deaths.values - recovered.values,
    "Recovered": recovered
})

N = total_df.sum(axis=1)
total_df['Healthy'] = N.max() - N

x = np.arange(1, len(total_df) + 1)
y = confirmed
x_log = np.log(x)
y_log = np.log(y)

m, b = np.polyfit(x_log, y_log, 1)

y_fit_log = m * x_log + b
y_fit = np.exp(y_fit_log)

plt.plot(x, total_df["Active"] + total_df["Recovered"] + total_df["Deaths"], 'o')
plt.plot(x, y_fit)
plt.title("Global Confirmed Cases")
plt.xlabel("Time (Days)")
plt.ylabel("# Confirmed Cases")
plt.legend(["Raw Data", "Best Fit Line"])
plt.xscale("log")
plt.yscale("log")
plt.savefig(os.path.join(output_path, "COVID-19_confirmed.png"))

total_df[["Deaths", "Active", "Healthy", "Recovered"]].plot.area(title="Global Case Breakdown Over Time", colormap="RdYlGn")
plt.savefig(os.path.join(output_path, "COVID-19.png"))