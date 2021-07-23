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

import os
import requests
import json
from flask import Flask, send_file, jsonify, request
from whitenoise import WhiteNoise
from .backend import collab, email_employee
from .backend import azure
from .backend import security, database

REQUIRED_VARS = ["app_id", "secret", "access_token", "WEBEX_BASE_URL",
                    "WEBEX_ACCESS_TOKEN", "WEBEX_BOT_TOKEN", "DUO_INTEGRATION_KEY", 
                    "DUO_SECRET_KEY", "DUO_DOMAIN", "cucm_ip", "cucm_username", 
                    "cucm_password", "MONGO_USER", "MONGO_PASS", "WEBEX_REFRESH_TOKEN"]

for var in REQUIRED_VARS:
    if var not in os.environ.keys():
        logger.error(f"Missing required environment variable {var}. Aborting.")
        sys.exit(-1)

app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root='/static', prefix='static')

@app.route("/")
def main():
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(BASE_PATH, "..", "static", "index.html")
    return send_file(index_path)

@app.route("/hello-flask")
def hello():
    return jsonify({'greeting':'Hello from Flask!'})

@app.route("/provision-user", methods=['GET', 'POST'])
def provision_user():
    products_collab = request.get_json(force=True)["products-collab"]
    products_na = request.get_json(force=True)["products-na"]
    products_sec = request.get_json(force=True)["products-sec"]
    user_name = request.get_json(force=True)["user-name"]
    user_items = request.get_json(force=True)["user-items"]
    user_mac = request.get_json(force=True)["mac-phone"]
    user_model = request.get_json(force=True)["model-phone"]

    col = False
    na = False
    sec = False

    status_message = {}
    database.write_string("neo-logs", "provision", {"LOG": f"Provisioning {user_name}"})

    collab.say_hello("stienvan@cisco.com", request.get_json(force=True))
    database.write_string("neo-logs", "provision", {"LOG": "Sent bot message to admin"})

    try:
        device_code = "null"
        if (len(json.loads(products_collab)) > 0):
            database.write_string("neo-logs", "provision", {"LOG": f"Provisioning {str(products_collab)}"})
            col = True
            lic_to_provision = collab.license_info(products_collab)
            device_code = collab.device_info(products_collab) #returns device registration code
            user_id = collab.user_info(user_items) 
            collab.phone_info(products_collab, user_mac, user_items, user_model)
            
            if (user_id == "null"):
                collab.add_member(lic_to_provision, user_items)
                status_message["Collab"] = ["Provisioned Webex user with appropriate licenses."]
            else: 
                status_message["Collab"] = ["User already exists in Control Hub"]

            
            if device_code == "null":
                status_message["Collab"] += ["No Webex device provisioned."]
            else:
                status_message["Collab"] += ["Webex device provisioned. Activation code: " + device_code]

                       
    except Exception as exc:
        database.write_string("neo-logs", "provision", {"LOG": f"Exception in COLLAB: {str(exc.args)}"})
        return jsonify({"Exception in COLLAB" : exc.args})

    user_info = json.loads(user_items)

    try:
        if (len(json.loads(products_na)) > 0):
            database.write_string("neo-logs", "provision", {"LOG": f"Provisioning {str(products_na)}"})
            na = True
            status_message["NA"] = ["Included organization ID and Meraki URL in employee email."]
    except Exception as exc:
        database.write_string("neo-logs", "provision", {"LOG": f"Exception in NETWORK ACCESS: {str(exc.args)}"})
        return jsonify({"Exception in NETWORK ACCESS" : exc.args})

    try:
        duo_users = []
        if (len(json.loads(products_sec)) > 0):
            database.write_string("neo-logs", "provision", {"LOG": f"Provisioning {str(products_sec)}"})
            sec = True
            duo_users_id = security.get_user_duo(user_info)

            if (duo_users_id == "Null"):
                security.create_users_duo(user_info) #else we should tell the admin the email is already enrolled
                status_message["Security"] = ["User was provisioned for Duo services."]
                status_message["Security"] += ["Automatic activation email for Duo sent to employee."]
            else: 
                status_message["Security"] = ["User already exists in duo"]
            
            

    except Exception as exc:
        database.write_string("neo-logs", "provision", {"LOG": f"Exception in SEC: {str(exc.args)}"})
        return jsonify({"Exception in SEC" : exc.args})
 
    try: 
        database.write_string("neo-logs", "provision", {"LOG": f"Sending email to user"})
        email_employee.emailEmpl(user_info['email'], user_info['lname'], user_info['fname'], str(device_code), col, na, sec)
    except Exception as exc:
        database.write_string("neo-logs", "provision", {"LOG": f"Exception in EMAIL: {str(exc.args)}"})
        return jsonify({"Exception in EMAIL" : exc.args})

    return jsonify(status_message)

@app.route("/deprovision-user", methods=['GET', 'POST'])
def deprovision_user():
    user_name = request.get_json(force=True)["user-name"]
    user_items = request.get_json(force=True)["user-items"]

    user_id = collab.user_info(user_items) 
    if (user_id != "null"):
        collab.delete_member(user_id)

    return jsonify({"greeting": "Deprovisioned user"})

@app.route("/list-users", methods=['GET'])
def list_users():
    list_users_azure = azure.return_users()
    return jsonify(list_users_azure)

@app.route("/delete-users", methods=['GET', 'POST'])
def del_user():
    user_selected = request.get_json(force=True)["user"]
    user_id = collab.user_info(user_selected) 
    
    if (user_id != "null"):
        collab.delete_member(user_id)
    
    return 

@app.route("/dashboard-data", methods=['GET'])
def dashboard_data():
    try: 
        dashboard_info = {}
        dashboard_info['no_collab_users'] = collab.collab_dashboard_info()
        dashboard_info['no_collab_devices'] = collab.device_dashboard_info()
        dashboard_info['no_duo_users'] = security.duo_dashboard_info()
    except Exception as exc:
        return jsonify(exc.args)
    return jsonify(dashboard_info)