import os

config = {}

config['WEBEX_BASE_URL'] = os.environ['WEBEX_BASE_URL']
config['WEBEX_ACCESS_TOKEN'] = os.environ['WEBEX_ACCESS_TOKEN']
config['WEBEX_REFRESH_TOKEN'] = os.environ['WEBEX_REFRESH_TOKEN']
config['WEBEX_BOT_TOKEN'] = os.environ['WEBEX_BOT_TOKEN']

config['cucm_ip'] = os.environ['cucm_ip']
config['cucm_username'] = os.environ['cucm_username']
config['cucm_password'] = os.environ['cucm_password']

config['app_id'] = os.environ['app_id']
config['secret'] = os.environ['secret']
config['access_token']= os.environ['access_token']

config['DUO_INTEGRATION_KEY'] = os.environ['DUO_INTEGRATION_KEY']
config['DUO_SECRET_KEY'] = os.environ['DUO_SECRET_KEY']
config['DUO_DOMAIN'] = os.environ['DUO_DOMAIN']

config['MONGO_USER'] = os.environ['MONGO_USER']
config['MONGO_PASS'] = os.environ['MONGO_PASS']