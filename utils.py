import requests
from requests.exceptions import HTTPError
import os
import csv

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
    get_enigma_data('b2cda379-c500-4ef5-aa2a-2dfae29e3aff', os.environ["ENIGMA_API_KEY"])

if __name__ == "__main__":
    main()