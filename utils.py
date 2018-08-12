"""
This provides helper methods to pull and manipulate data from enigma.com
"""
import os
import io
import warnings
import requests
from requests.exceptions import HTTPError
import pandas as pd
import geopy
from geopy import geocoders
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams

warnings.filterwarnings('ignore')

DATASET_ID = 'f93ffd80-6679-4a76-a86e-2ab1f4007815'

def get_enigma_data(dataset_id, api_key):
    """
    get_enigma_data takes a dataset id and returns the associated csv content
    """

    base_url = "https://public.enigma.com/api/"
    headers = {'authorization': 'Bearer {}'.format(api_key)}
    url = base_url + 'datasets/{}'.format(dataset_id)
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
    except HTTPError:
        print 'Request to url {} returned with status code {}'.format(resp.url, resp.status_code)
        return None

    snapshot_id = resp.json()['current_snapshot']['id']

    url = base_url + 'export/{}'.format(snapshot_id)
    try:
        dat = requests.get(url, headers=headers).content.decode('utf-8')
        resp.raise_for_status()
    except HTTPError:
        print 'Request to url {} returned with status code {}'.format(resp.url, resp.status_code)
        return None

    return dat

def get_coords(dat):
    """
    get_coords appends the coordinates as rows to the data set using the
    google maps api
    """
    geopy.geocoders.options.default_timeout = 3
    g_coder = geocoders.GoogleV3(os.environ['GOOGLE_API_KEY'])

    bad_rows = []
    for i, row in dat.iterrows():
        try:
            location = g_coder.geocode(row['event_location'])
            if not location:
                bad_rows.append(i)
            else:
                dat.loc[i, 'long'] = location.longitude
                dat.loc[i, 'lat'] = location.latitude
        except Exception as e:
            print e
            bad_rows.append(i)

    # Remove rows that couldn't geocode due to bad event location
    dat.drop(dat.index[bad_rows])
    return dat


def overview():
    """
    prints descriptive statistics for event data
    """
    dat = get_enigma_data(DATASET_ID, os.environ['ENIGMA_API_KEY'])
    event_data = pd.read_csv(io.StringIO(dat))

    print event_data["event_name"].value_counts()
    print event_data["event_agency"].value_counts()
    print event_data["event_location"].value_counts()
    print event_data["event_borough"].value_counts()
    print event_data["event_type"].value_counts()

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
