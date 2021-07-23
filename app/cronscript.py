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
import os, requests

def update_Admin(messageToAdmin):
    s = requests.Session()
    s.headers.update({
        'Authorization': "Bearer " + os.environ['WEBEX_BOT_TOKEN']
    })

    WEBEX_BASE_URL = "https://webexapis.com"
    url = f"{WEBEX_BASE_URL}/v1/messages"

    data = {
        "toPersonEmail": "stienvan@cisco.com",
        "text": messageToAdmin, 
    }

    resp = s.post(url, json=data)
    resp.raise_for_status()

url = "https://webexapis.com/v1/access_token"

payload='grant_type=refresh_token&client_id=C91eb42821df0d8d205d90cd27cedfb004eeff6b787054578647f1baa7eb70868&client_secret=8ad397e278d9f6392739fb109da69d9bf35fb1dfc9b40ff66fdb9c8dc4e2d2dc&refresh_token=' + os.environ['WEBEX_REFRESH_TOKEN']
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)
if response.status_code == 200 or response.status_code == 204 :
    print(response.text)
    access_token = response.json()['access_token']
    refresh_token = response.json()['refresh_token']
    print(access_token)
    os.environ["WEBEX_ACCESS_TOKEN"] = access_token
    os.environ["WEBEX_REFRESH_TOKEN"] = refresh_token
    update_Admin('Hello, New access tocken has been generated for the new-employee-onboarding integration. Access Token: ' + access_token + ' Refresh token: ' + refresh_token)
else :
    update_Admin('Hello, the cronjob was not able to generate new access tocken for the new-employee-onboarding integration. Here is the response code : ' + 
    str(response.status_code) + '.')



# samlpe response text below. access_token is the newly generated token
# {
#     "access_token": "YjgzYzA3OTctN2RiNy00MWY4LWIyOWUtZTNlY2Y4ZDNhNjdlNWY4NDYwNWYtZGY0_P0A1_36252b39-4c39-48c5-933f-afa3bbc77901",
#     "expires_in": 1209599,
#     "refresh_token": "OTVmNjFiZjEtYmM1ZS00NWU4LWJmOWUtMTBkMDlkMGM2NTI3YWM3YjI3MzEtODNk_P0A1_36252b39-4c39-48c5-933f-afa3bbc77901",
#     "refresh_token_expires_in": 6435474
# }

print('*** Ran the cron script ***')
