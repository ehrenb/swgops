# Utility API for obtaining and performing pre-processing on GalaxyHarvester resource data

import csv
import os
import shutil
from enum import Enum

import requests

# GH uses an integer value for the server to filter resources for
class GHServer(Enum):
    FINALIZER = 118

# gh base url
base_url = 'https://www.galaxyharvester.net/exports/current{server}.{ext}'

# location for data
data_dir = os.path.join(os.path.expanduser("~"), "data")

def download_file(url):
    """https://stackoverflow.com/a/16696317"""
    print(f'dowloading {url}')
    local_filename = url.split('/')[-1] + '.new'
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

# def get_current_xml(server=GHServer.FINALIZER):
#     previous_file = os.path.join(data_dir, f'current{server.value}.xml')
#     url = base_url.format(server=server.value, ext='xml')
#     new_file = download_file(url)
    
#     # previous is now current
#     shutil.move(new_file, previous_file)


def get_current_csv(server=GHServer.FINALIZER):
    previous_file = os.path.join(data_dir, f'current{server.value}.csv')
    url = base_url.format(server=server.value, ext='csv')
    new_file = download_file(url)

    previous_rows = []
    # record previous rows, if any
    if os.path.isfile(previous_file):
        with open(previous_file, 'r') as pf:
            previous_csvreader = csv.reader(pf)
            header = next(previous_csvreader)
            previous_rows = [row for row in previous_csvreader]

    # the diff in rows
    new_rows = []

    # open new, compare against prev, if any
    with open(new_file, 'r') as nf:
        new_csvreader = csv.reader(nf)
        header = next(new_csvreader)

        for row in new_csvreader:
            if row not in previous_rows:
                # print(f"{row} is new!")
                new_rows.append(row)

    # print(header)

    # convert the diff result to dictionary
    new_rows_dicts = []
    for r in new_rows:
        new_resource_dict = {}
        for idx, hr, in enumerate(header):
            new_resource_dict[hr] = r[idx]
        new_rows_dicts.append(new_resource_dict)

    # previous is now current
    # print(f'moving file to {previous_file}')
    shutil.move(new_file, previous_file)

    return new_rows_dicts

