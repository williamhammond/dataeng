"""
visualize reads the generated dataset and maps the locations of events
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd

def plot_events(dat):
    """
    plot events displays a map of events
    """
    new_style = {'grid': False}
    matplotlib.rc('axes', **new_style)
    rcParams['figure.figsize'] = (17.5, 17)
    rcParams['figure.dpi'] = 250

    dat.plot(kind='scatter', x='long', y='lat', color='black',
             xlim=(-74.06, -73.77), ylim=(40.61, 40.91), s=.02, alpha=.6)
    plt.savefig('./reports/event_locations.png')

def main():
    """
    request dataset of events happening in nyc
    """
    dat = pd.read_csv("./data/processed/events.csv")
    plot_events(dat)

if __name__ == "__main__":
    main()
