import os
import glob
import numpy as np
import pandas as pd
from git import Repo
from matplotlib import pyplot as plt

def create_graph(confirmed, deaths, recovered, output_path, identifier):
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

    x = np.arange(len(total_df) - 13, len(total_df) + 1)
    y = confirmed[-14:]
    x_log = np.log(x)
    y_log = np.log(y)

    m, b = np.polyfit(x_log, y_log, 1)

    y_fit_log = m * x_log + b
    y_fit = np.exp(y_fit_log)

    plt.plot(x, y, 'o')
    plt.plot(x, y_fit)
    plt.title(identifier + " Confirmed Cases")
    plt.xlabel("Time (Days)")
    plt.ylabel("# Confirmed Cases")
    plt.legend(["Raw Data", "Best Fit Line (y = {}*x^{})".format(round(np.exp(b), 2), round(m, 2))])
    plt.xscale("log")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "COVID-19_" + identifier + "_confirmed.png"))
    plt.clf()

    total_df[["Deaths", "Active", "Healthy", "Recovered"]].plot.area(title= identifier + " Case Breakdown Over Time", colormap="RdYlGn")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "COVID-19_" + identifier + "_breakdown.png"))
    plt.clf()


if __name__ == "__main__":
    repo_path = "../"
    data_root = "./COVID-19/csse_covid_19_data/csse_covid_19_time_series/"
    output_path = "../assets/images/"

    repo = Repo(repo_path)
    output = repo.git.submodule('update', '--remote')

    confirmed = pd.read_csv(os.path.join(data_root, "time_series_covid19_confirmed_global.csv"))
    deaths = pd.read_csv(os.path.join(data_root, "time_series_covid19_deaths_global.csv"))
    recovered = pd.read_csv(os.path.join(data_root, "time_series_covid19_recovered_global.csv"))
    us_confirmed = confirmed[confirmed["Country/Region"] == "US"]
    us_deaths = deaths[deaths["Country/Region"] == "US"]
    us_recovered = recovered[recovered["Country/Region"] == "US"]
    nl_confirmed = confirmed[confirmed["Country/Region"] == "Netherlands"]
    nl_deaths = deaths[deaths["Country/Region"] == "Netherlands"]
    nl_recovered = recovered[recovered["Country/Region"] == "Netherlands"]
    
    create_graph(confirmed, deaths, recovered, output_path, "Global")
    create_graph(us_confirmed, us_deaths, us_recovered, output_path, "US")
    create_graph(nl_confirmed, nl_deaths, nl_recovered, output_path, "Netherlands")

