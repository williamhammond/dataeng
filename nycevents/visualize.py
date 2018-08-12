"""
visualize reads the generated dataset and maps the locations of events
"""
import io
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
from nycevents.make_dataset import get_coords, get_enigma_data

DATASET_ID = 'f93ffd80-6679-4a76-a86e-2ab1f4007815'

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
    plt.show()

def main():
    """
    request dataset of events happening in nyc
    """
    dat = get_enigma_data(DATASET_ID, os.environ['ENIGMA_API_KEY'])
    event_data = pd.read_csv(io.StringIO(dat))
    dat = get_coords(event_data)
    dat.to_csv('./events.csv')
    plot_events(dat)

if __name__ == "__main__":
    main()
