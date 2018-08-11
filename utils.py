"""
This provides helper methods to pull and manipulate data from enigma.com
"""
import os
import io
import requests
from requests.exceptions import HTTPError
import pandas as pd

def get_enigma_data(dataset_id, api_key):
    """
    get_enigma_data takes a dataset id and returns the associated csv
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

def main():
    """
    request dataset of events happening in nyc
    """
    dat = get_enigma_data('f93ffd80-6679-4a76-a86e-2ab1f4007815', os.environ['ENIGMA_API_KEY'])
    event_data = pd.read_csv(io.StringIO(dat))

    print event_data["event_name"].value_counts()

if __name__ == "__main__":
    main()
