import requests
from typing import Dict

# never use this token to perform any Delete requests
# never use the token outside of this file
DUMMY_MOOCLET_API_TOKEN = "db071db130485666bfd39ac15b9dc1eb9d75f9cc"
DUMMY_MOOCLET_URL = "https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/"

POLICY_NAME_TO_ID = {"thompson_sampling_contextual": 6, 
                     "choose_policy_group": 12,
                     "ts_configurable": 17}

class MoocletConnector:

    def __init__(self, mooclet_id=-1, token=DUMMY_MOOCLET_API_TOKEN, url=DUMMY_MOOCLET_URL):
        self.token = token
        self.url = url
        self.mooclet_id = mooclet_id

        if mooclet_id != -1:  # unknown mooclet_id; intended for create mooclet
            try:
                self.get_mooclet()
            except requests.HTTPError as e:
                raise


    def create_mooclet(self, mooclet_name: str, policy_name: str) -> Dict:
        endpoint = "mooclet"
        params = {"policy": POLICY_NAME_TO_ID[policy_name],  # policy id
                  "name": mooclet_name}

        objects = requests.post(
            url = self.url + endpoint,
            data = params,
            headers = {'Authorization': f'Token {self.token}'}
        )

        try:
            objects.raise_for_status()
        except requests.HTTPError as e:
            print("Error: " + str(e))
            raise

        return objects.json()


    def get_mooclet(self) -> Dict:
        endpoint = "mooclet"
        objects = requests.get(
            url = self.url + endpoint + "/" + str(self.mooclet_id),
            headers = {'Authorization': f'Token {self.token}'}
        )

        try:
            objects.raise_for_status()
        except requests.HTTPError as e:
            print("Error: " + str(e))
            raise

        return objects.json()
    

    def get_versions(self) -> Dict:
        endpoint = "version-name"
        params = {"mooclet": self.mooclet_id}
        objects = requests.get(
            url = self.url + endpoint,
            params = params,
            headers = {'Authorization': f'Token {self.token}'}
        )

        try:
            objects.raise_for_status()
        except requests.HTTPError as e:
            print("Error: " + str(e))
            raise

        return objects.json()


    def get_policy_parameters(self) -> Dict:
        endpoint = "policyparameters"
        params = {"mooclet": self.mooclet_id}
        objects = requests.get(
            url = self.url + endpoint,
            params = params,
            headers = {'Authorization': f'Token {self.token}'}
        )

        try:
            objects.raise_for_status()
        except requests.HTTPError as e:
            print("Error: " + str(e))
            raise

        return objects.json()
    

    def create_policy_parameters(self, policy_id: int, parameters: Dict) -> Dict:
        endpoint = "policyparameters"
        params = {
            "mooclet": self.mooclet_id,
            "policy": policy_id,
            "parameters": parameters
        }
        objects = requests.post(
            url = self.url + endpoint,
            data = params,
            headers = {'Authorization': f'Token {self.token}'}
        )

        try:
            objects.raise_for_status()
        except requests.HTTPError as e:
            print("Error: " + str(e))
            raise

        return objects.json() 


    def get_values(self) -> Dict:
        endpoint = "value"
        params = {"mooclet": self.mooclet_id}

        objects = requests.get(
            url = self.url + endpoint,
            params = params,
            headers = {'Authorization': f'Token {self.token}'}
        )

        try:
            objects.raise_for_status()
        except requests.HTTPError as e:
            print("Error: " + str(e))
            raise

        return objects.json()


    def get_policy_parameters_history(self) -> Dict:
        endpoint = "policyparametershistory"
        params = {"mooclet": self.mooclet_id}
        objects = requests.get(
            url = self.url + endpoint,
            params = params,
            headers = {'Authorization': f'Token {self.token}'}
        )

        try:
            objects.raise_for_status()
        except requests.HTTPError as e:
            print("Error: " + str(e))
            raise

        return objects.json()
    
#mooclet = MoocletConnector(25)

# new_mooclet_id = mooclet.create_mooclet("301 " + str(datetime.datetime.now()), 
#                                         "thompson_sampling_contextual")
# mooclet.get_mooclet(new_mooclet_id)
