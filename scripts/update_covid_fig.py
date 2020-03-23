import os
import numpy as np
import pandas as pd
from git import Repo
from matplotlib import pyplot as plt

repo_path = "../"
data_root = "./COVID-19/csse_covid_19_data/csse_covid_19_time_series/"
output_path = "../assets/images/COVID-19.png"

repo = Repo(repo_path)

for submodule in repo.submodules:
    submodule.update(init=True)

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

total_df[['Deaths', 'Confirmed', 'Healthy', 'Recovered']].plot.area(title="Global Case State Over Time", colormap="RdYlGn")
plt.savefig(output_path)
