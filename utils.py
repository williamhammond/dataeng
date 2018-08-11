import requests
from requests.exceptions import HTTPError
import os
import csv
import io
import pandas as pd

def get_enigma_data(dataset_id, api_key):
    """
    get_enigma_data takes a dataset id and returns the associated csv
    """
    
    base_url = "https://public.enigma.com/api/"
    headers = {'authorization': 'Bearer {}'.format(api_key)}
    url = base_url + 'datasets/{}'.format(dataset_id)
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except HTTPError:
        print 'Request to url {} returned with status code {}'.format(r.url, r.status_code)
        return 
    
    snapshot_id = r.json()['current_snapshot']['id']

    url = base_url + 'export/{}'.format(snapshot_id)
    try:
        dat = requests.get(url, headers=headers).content.decode('utf-8')
        r.raise_for_status()
    except HTTPError:
        print 'Request to url {} returned with status code {}'.format(r.url, r.status_code)
        return 

    return dat

def main():
    d = get_enigma_data('f93ffd80-6679-4a76-a86e-2ab1f4007815', os.environ['ENIGMA_API_KEY'])
    df = pd.read_csv(io.StringIO(d))
    print df

if __name__ == "__main__":
    main()