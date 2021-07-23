"""Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from O365 import Account
import requests
import json
import os
from .env import config

def return_users(): 
  credentials = (config['app_id'], config['secret'])

  scopes = ['User.Read.All']  # you can use scope helpers here (see Permissions and Scopes section)
  account = Account(credentials, auth_flow_type='credentials', tenant_id='b59f4de7-1881-4184-b182-0b5ae4109c7b')
  if account.authenticate():
    print('Authenticated!')

  with open('o365_token.txt', 'r') as fobj:
    data = json.load(fobj)

  #token=data["access_token"]
  config['access_token'] = data["access_token"]
  #print(config['access_token'])

  filename='o365_token.txt'
  if os.path.exists(filename): os.remove(filename)

  url = "https://graph.microsoft.com/v1.0/users"

  payload={}
  headers = {
    'Content-Type': 'application/json',
    'Authorization': f"Bearer {config['access_token']}"
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  json_data = json.loads(response.text)
  print(json_data)
  result = []
  for value in response.json()['value']:
    print(value['givenName'])
    result.append({
      "fname" : value['givenName'],
      "lname" : value['surname'],
      "email" : value['mail'],
      "mobilephone" : value['businessPhones']
    })

  return result

# a,b,c,d = return_users()    
# print(a)

# print(return_users())



# x= return_users()
# print(x)
