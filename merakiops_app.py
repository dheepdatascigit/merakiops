# This is meraki api application for Operating Meraki.
# Author: Dheep <dheepvijay@gmail.com>
# Version: v0.01

"""
Version History

V1: List devices
    - Draft version for connecting to meraki and list networks and devices
"""

import csv
import pandas
import requests
import json


def get_api_creds(apikeycsvfile):
    """ get api key and org_id from file

    syntax: get_api_creds("key_filename")
    output: dictionary of the api_key and org_id

    The file should have only two lines in below format
    api_key,org_id
    <your api key>,<your org id>

    """

    api_access = {}

    df = pandas.read_csv(apikeycsvfile)
    api_access = df.to_dict('records')
    print(type(api_access[0]), api_access[0])

    return api_access[0]


instance_apikey = get_api_creds('accessapi.key')

print(instance_apikey)

api_key = instance_apikey['api_key']
org_id = str(instance_apikey['org_id'])
org_url = 'https://dashboard.meraki.com/api/v0/organizations'
meraki_headers = {'x-cisco-meraki-api-key': api_key, 'content-type': 'application/json'}
# get all of the organizations this api key has access to
response = requests.get(org_url, headers=meraki_headers)
json_output = json.loads(response.text)
# loop through the json_output and print each row
for row in json_output:
    print(row)
    print("Org ID: " + str(row['id']))
    print("Org Name: " + row['name'])

print(type(org_id))

network_url = 'https://api.meraki.com/api/v0/organizations/' + org_id + '/networks'
print(network_url)
response = requests.get(network_url, headers=meraki_headers)
json_output = json.loads(response.text)

for row in json_output:
    print(row)
