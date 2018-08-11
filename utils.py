import requests
import os
import csv

def get_enigma_data(dataset_id, api_key):
    """
    get_enigma_data takes a dataset id and returns the associated csv
    """
    
    base_url = "https://public.enigma.com/api/"
    headers = {'authorization': 'Bearer {}'.format(api_key)}
    url = base_url + 'datasets/{}'.format(dataset_id)
    r = requests.get(url, headers=headers)
    snapshot_id = r.json()['current_snapshot']['id']

    url = base_url + 'export/{}'.format(snapshot_id)
    dat = requests.get(url, headers=headers).content.decode('utf-8')

    return dat

def main():
    get_enigma_data('', os.environ["ENIGMA_API_KEY"])

if __name__ == "__main__":
    main()