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

import duo_client
import json
from .env import config

def get_user_duo(user):
    admin_api = duo_client.Admin(
        ikey=config["DUO_INTEGRATION_KEY"],
        skey=config["DUO_SECRET_KEY"],
        host=config["DUO_DOMAIN"],
    )
    # admin_api.set_proxy(host="")
    
    duo_id = "Null"
    resp = admin_api.get_users()
    for items in resp:
        if (items["email"]== user["email"]):
           duo_id = items['user_id'] 

    return duo_id


def delete_user_duo(id):
    admin_api = duo_client.Admin(
        ikey=config["DUO_INTEGRATION_KEY"],
        skey=config["DUO_SECRET_KEY"],
        host=config["DUO_DOMAIN"],
    )
    # admin_api.set_proxy(host="")

    resp = admin_api.delete_user(id)

    return resp

def create_users_duo(user):
    admin_api = duo_client.Admin(
        ikey=config["DUO_INTEGRATION_KEY"],
        skey=config["DUO_SECRET_KEY"],
        host=config["DUO_DOMAIN"],
    )
    # admin_api.set_proxy(host="")
    username = user['fname'] + user['lname']

    resp = admin_api.add_user(username, None, None, None, user['email'])
    enroll = admin_api.enroll_user(username, user['email'])

    return resp

def duo_dashboard_info():
    admin_api = duo_client.Admin(
        ikey=config["DUO_INTEGRATION_KEY"],
        skey=config["DUO_SECRET_KEY"],
        host=config["DUO_DOMAIN"],
        sig_timezone="Africa/Blantyre"
    )
    # admin_api.set_proxy(host="")
    
    counter_duo = 0
    resp = admin_api.get_users()
    for items in resp:
        counter_duo = counter_duo + 1

    return counter_duo