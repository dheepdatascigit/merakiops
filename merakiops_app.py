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

def get_api_call(apiurl, urlheaders):
    """ Make an API call and return as dictionary

    Syntax: get_api_call('api url', 'headers')
    output: return_code, dictionary of JSON object returned.

    """

    print (apiurl, urlheaders)
    response = requests.get(apiurl, headers=urlheaders)
    json_output = json.loads(response.text)
    return response, json_output
    # return '200', {'id':'1', 'name':'test'}


instance_apikey = get_api_creds('accessapi.key')

print(instance_apikey)

api_key = instance_apikey['api_key']
org_id = str(instance_apikey['org_id'])

meraki_api_url = 'https://dashboard.meraki.com/api/v0/'
meraki_headers = {'x-cisco-meraki-api-key': api_key, 'content-type': 'application/json'}

org_url = meraki_api_url + 'organizations'

# get all of the organizations this api key has access to
# response = requests.get(org_url, headers=meraki_headers)
# json_output = json.loads(response.text)

# loop through the json_output and print each row
rcode, json_dict = get_api_call(org_url, meraki_headers)
for row in json_dict:
    print(row, type(row))
    print(rcode, type(rcode))
    print("Org ID: " + str(row['id']))
    print("Org Name: " + row['name'])

print(type(org_id))

network_url = 'https://api.meraki.com/api/v0/organizations/' + org_id + '/networks'
print(network_url)

rcode, json_dict = get_api_call(network_url, meraki_headers)
print(json_dict)
for row in json_dict:
    print(row)
    print(row['id'])
    vlan_network_url = 'https://api.meraki.com/api/v0/networks/' + row['id'] + '/devices'
    print(vlan_network_url)
    
    vlanrcode, vlan_json_dict = get_api_call(vlan_network_url, meraki_headers)
    print("\n\n")
    print(vlan_json_dict)
    for item in vlan_json_dict:
        dev_url = 'https://api.meraki.com/api/v0/devices/' + item['serial'] + '/clients?timespan=7200'
        #/devices/[serial]/clients

        clientrcode, client_json_dict = get_api_call(dev_url, meraki_headers)
        
        print("\n\n")
        # print(client_json_output)
        for i in client_json_dict:
            print(i)
            print(i['dhcpHostname'], i['description'], i['ip'])

