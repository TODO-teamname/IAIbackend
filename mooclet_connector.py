import requests
import datetime

# hide the api token when pushing to github or deployment
# MOOCLET_API_TOKEN = 

POLICY_NAME_TO_ID = {"thompson_sampling_contextual": 6, 
                     "choose_policy_group": 12,
                     "ts_configurable": 17}

class MoocletConnector:
    def __init__(self, token = MOOCLET_API_TOKEN):
        self.token = MOOCLET_API_TOKEN
        self.url = "https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/"

    def get_mooclet(self, mooclet_id = 25):
        endpoint = "mooclet"
        objects = requests.get(
            url = self.url + endpoint + "/" + str(mooclet_id),
            headers = {'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 200:
            print("unable to get mooclet")
            print(objects.json())
        else:
            print(objects.json())
            print(objects.json()["id"])
            return objects.json()["id"]
    
    def create_mooclet(self, mooclet_name, policy_name):
        endpoint = "mooclet"
        params = {"policy": POLICY_NAME_TO_ID[policy_name],  # policy id
                  "name": mooclet_name}
        objects = requests.post(
            url = self.url + endpoint,
            data = params,
            headers = {'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 201:
            print("unable to create mooclet")
            print(objects.json())
        else:
            print(objects.json())
            print(objects.json()["id"])
            return objects.json()["id"]



mooclet = MoocletConnector()
mooclet.get_mooclet()  # default get mooclet id=25
new_mooclet_id = mooclet.create_mooclet("301 " + str(datetime.datetime.now()), 
                                        "thompson_sampling_contextual")
mooclet.get_mooclet(new_mooclet_id)
