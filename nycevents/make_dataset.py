"""
make_dataset pulls data from enigma.com and and then supplements the
data with longitude and latitude information for visualization
"""
import os
import io
import requests
from requests.exceptions import HTTPError
import pandas as pd
import geopy
from geopy import geocoders
from geopy.exc import GeocoderTimedOut

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

def overview(event_data):
    """
    prints descriptive statistics for event data
    """
    print event_data["event_name"].value_counts()
    print event_data["event_agency"].value_counts()
    print event_data["event_location"].value_counts()
    print event_data["event_borough"].value_counts()
    print event_data["event_type"].value_counts()

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
        except GeocoderTimedOut as err:
            print "Error: geocode failed on %s with message %s"%(row['event_location'], err.message)
            bad_rows.append(i)

    # Remove rows that couldn't geocode due to bad event location
    dat.drop(dat.index[bad_rows])
    return dat

def main():
    """
    request dataset of events happening in nyc
    """
    dat = get_enigma_data(DATASET_ID, os.environ['ENIGMA_API_KEY'])
    event_data = pd.read_csv(io.StringIO(dat))
    event_data.to_csv('./data/raw/events.csv')
    dat = get_coords(event_data)
    dat.to_csv('./data/processed/events.csv')


if __name__ == "__main__":
    main()
