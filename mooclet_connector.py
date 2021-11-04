import requests
import datetime

# never use this token to perform any Delete requests
# never use the token outside of this file
MOOCLET_API_TOKEN = "db071db130485666bfd39ac15b9dc1eb9d75f9cc"

POLICY_NAME_TO_ID = {"thompson_sampling_contextual": 6, 
                     "choose_policy_group": 12,
                     "ts_configurable": 17}


class MoocletConnector:

    def __init__(self, mooclet_id = -1, token = MOOCLET_API_TOKEN):
        self.token = MOOCLET_API_TOKEN
        self.url = "https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/"
        
        self.mooclet_id = mooclet_id
        if mooclet_id != -1:  # unknown mooclet_id; intended for create mooclet
            res_status = self.get_mooclet()
            if res_status != 200:  # mooclet_id not found in the MOOClet Engine DB
                self.mooclet_id = -1
                print("Error: invalid mooclet id given")


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
            self.mooclet_id = objects.json()["id"]  # attach this new mooclet_id
            return objects.json()["id"]


    def get_mooclet(self):
        endpoint = "mooclet"
        objects = requests.get(
            url = self.url + endpoint + "/" + str(self.mooclet_id),
            headers = {'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 200:
            print("unable to get mooclet")
            print(objects.json())
        else:
            print(objects.json())
            print(objects.json()["id"])
            return objects.status_code
    

    def get_versions(self):
        endpoint = "version-name"
        params = {"mooclet": self.mooclet_id}
        objects = requests.get(
            url = self.url + endpoint,
            params = params,
            headers = {'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 200:
            print("unable to get mooclet versions")
            print(objects.json())
        else:
            print(objects.json())


    def get_policy_parameters(self):
        endpoint = "policyparameters"
        params = {"mooclet": self.mooclet_id}
        objects = requests.get(
            url = self.url + endpoint,
            params = params,
            headers = {'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 200:
            print("unable to get mooclet policy parameters")
            print(objects.json())
        else:
            print(objects.json())


    def get_values(self):
        endpoint = "value"
        params = {"mooclet": self.mooclet_id}
        objects = requests.get(
            url = self.url + endpoint,
            params = params,
            headers = {'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 200:
            print("unable to get mooclet values")
            print(objects.json())
        else:
            print(objects.json())


    def get_policy_parameters_history(self):
        endpoint = "policyparametershistory"
        params = {"mooclet": self.mooclet_id}
        objects = requests.get(
            url = self.url + endpoint,
            params = params,
            headers = {'Authorization': f'Token {self.token}'}
        )
        print(objects.status_code)
        if objects.status_code != 200:
            print("unable to get mooclet policy parameters history")
            print(objects.json())
        else:
            print(objects.json())
    


print("setting up mooclet")
mooclet = MoocletConnector(25)
print("getting mooclet info")
mooclet.get_mooclet()  # default get mooclet id=25
print("getting mooclet version")
mooclet.get_versions()
print("getting mooclet associated values")
mooclet.get_values()
print("getting mooclet policy parameters")
mooclet.get_policy_parameters()
print("getting mooclet policy parameters history")
mooclet.get_policy_parameters_history()

# new_mooclet_id = mooclet.create_mooclet("301 " + str(datetime.datetime.now()), 
#                                         "thompson_sampling_contextual")
# mooclet.get_mooclet(new_mooclet_id)
