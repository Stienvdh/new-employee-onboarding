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

import pymongo
import json
from .env import config

def write_string(database, collection, value):
    client = pymongo.MongoClient(f"mongodb://{config['MONGO_USER']}:{config['MONGO_PASS']}@db:27017/?compressors=disabled&gssapiServiceName=mongodb")
    db = client[database]
    col = db[collection] 

    try:
        col.insert_one(value)
    except Exception as exc:
        return str(exc)
    
    client.close()
    return "Logged to database"
        