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

import requests
from .env import config
from .database import write_string
import json
import datetime
from ciscoaxl import axl


def license_info(products):
    products = json.loads(products)
    session = requests.Session()
    session.headers.update({
        'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
    })

    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/licenses"
    resp = session.get(url)

    print(resp.status_code)
    if resp.status_code == 200:
        print("Success")
    
    
    license_list = []
    for name in products:
        if (name == 'Provision Meetings'):
            license_list += ['Meeting - Webex Enterprise Edition']
        elif (name == 'Provision Messaging'):
            license_list += ['Messaging']
        
    license_list += ["Free screen share"]
    license_list += ["Free meeting"]
    license_list += ["Free message"]
    license_list += ['Call on Webex']

    license_ids = []
    for lic in resp.json()['items']:
        if (lic['name'] in license_list):
            license_ids.append(lic["id"])
    
    return license_ids

def device_info(products):
    products = json.loads(products)
    code = "null"
    for name in products:
        if (name == "Provision Video Device"):
            id = place_id()
            code = device_code(id)
    
    return code

def add_member(lic, user):
    s = requests.Session()
    s.headers.update({
        'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
    })

    user = json.loads(user)
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/people"
    
    data = {
        
        "emails": [
            user['email']
        ],

        "phoneNumbers": [
            {
                "type": "work",
                "value": user['phone']
            }
        ],
        "displayName": user['fname'] + user['lname'],
        "firstName": user['fname'],
        "lastName": user['lname'],
        "licenses": lic
    }

    resp = s.post(url, json=data)

    print(resp.status_code)
    if resp.status_code == 200:
        print("Success")
    
    write_string("neo-logging", "collab", {"LOG" : f'Provisioned Webex for user at {datetime.datetime.now().isoformat()}'})
    
    return

def user_info(user):
    s = requests.Session()
    s.headers.update({
        'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
    })

    user = json.loads(user)
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/people"
    
    email = user['email']
    
    resp = s.get(url)

    user_id = "null"
    for items in resp.json()['items']:
        if(items['emails'][0] == email):
            user_id = items['id']
            
    print(resp.status_code)
    if resp.status_code == 200:
        print("Success")
    
    
    return user_id

def place_id():
    s = requests.Session()
    s.headers.update({
        'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
    })

    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/workspaces"
        
    resp = s.get(url)

    for items in resp.json()['items']:
        place_id = items['id']
            
    print(resp.status_code)
    if resp.status_code == 200:
        print("Success")
    
    
    return place_id

def device_code(placeId):
    s = requests.Session()
    s.headers.update({
        'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
    })

    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/devices/activationCode"
    
    payload = {
        "placeId":placeId
    }

    resp = s.post(url, json=payload)

    code = resp.json()['code']
        
            
    print(resp.status_code)
    if resp.status_code == 200:
        print("Success")
    
    
    return code
   
def delete_member(id):
    s = requests.Session()
    s.headers.update({
        'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
    })
    
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']


    url = f"{WEBEX_BASE_URL}/v1/people/{id}"
    resp = s.delete(url)

    print(resp.status_code)
    if resp.status_code == 200:
        print("Success")
    
    return

def say_hello(email, body):
    s = requests.Session()
    s.headers.update({
        'Authorization': f"Bearer {config['WEBEX_BOT_TOKEN']}"
    })

    WEBEX_BASE_URL = "https://webexapis.com"
    url = f"{WEBEX_BASE_URL}/v1/messages"

    data = {
        "toPersonEmail": "stienvan@cisco.com",
        "text": f'''
            Hello! I provisioned the following products for {body["user-name"]}:

            Collaboration: {body["products-collab"]}
            Network Access: {body["products-na"]}
            Security: {body["products-sec"]}

            Info used from Azure: {body["user-items"]}

            MAC Address inputted by admin: {body["mac-phone"]}
        ''',
    }

    resp = s.post(url, json=data)
    resp.raise_for_status()

def collab_dashboard_info():
    s = requests.Session()
    s.headers.update({
        'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
    })

    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/people"
    
    resp = s.get(url)
    counter = 0
    for items in resp.json()['items']:
        counter = counter + 1
        
    return counter

def device_dashboard_info():
    s = requests.Session()
    s.headers.update({
        'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
    })

    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/devices"
    
    resp = s.get(url)
    device_counter = 0
    for items in resp.json()['items']:
        device_counter = device_counter + 1
        
    return device_counter

def add_phone(mac, user, phone_type):

    cucm = config['cucm_ip']
    cucm_username = config['cucm_username']
    cucm_password = config['cucm_password']
    version = '12.5'
    ucm = axl(username=cucm_username,password=cucm_password,cucm=cucm,cucm_version=version)
    
    name = user['fname'] +" "+ user['lname']
    
    mac = mac[1:-1]
    phone_type = phone_type[1:-1]
    
    
    ext = user['phone']
    ext_final = ext[-4:]
    label = name +" - "+ ext_final

    prod = "Cisco " + phone_type
    prod_temp = "Standard " + phone_type + " SIP"

    ucm.add_directory_number(pattern=ext)
    ucm.add_phone(

        name='SEP' + mac,
        description='script_test',
        product=prod,
        device_pool='Default',
        location='Hub_None',
        phone_template=prod_temp,
        protocol='SIP',
        lines=[
            (ext, '', name, name, label, ext_final)
        ]
    )
    

    return

def phone_info(products, mac_add, userinfo, phone_model):
    products = json.loads(products)
    userinfo = json.loads(userinfo)

    for name in products:
        if (name == "Provision IP Phone"):
           add_phone(mac_add, userinfo, phone_model)
    
    
    return 




