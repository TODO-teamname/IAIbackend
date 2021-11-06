import requests
from typing import Dict

# never use this token to perform any Delete requests
# never use the token outside of this file
DUMMY_MOOCLET_API_TOKEN = "db071db130485666bfd39ac15b9dc1eb9d75f9cc"
DUMMY_MOOCLET_URL = "https://mooclet.canadacentral.cloudapp.azure.com/engine/api/v1/"

POLICY_NAME_TO_ID = {"thompson_sampling_contextual": 6, 
                     "choose_policy_group": 12,
                     "ts_configurable": 17}

def _mooclet_api_call(url, data={}, params={}, headers={}) -> Dict:
    objects = requests.get(
        url = url,
        data = data,
        params = params,
        headers = headers
    )

    try:
        objects.raise_for_status()
    except requests.HTTPError as e:
        print("Error: " + str(e))
        raise

    return objects.json()


class MoocletCreator:
    def __init__(self, token, url, mooclet_name, policy_name):
        self.token = token
        self.url = url
        self.mooclet_name = mooclet_name
        self.policy_name = policy_name
    
    def create_mooclet(self) -> Dict:
        endpoint = "mooclet"
        url = self.url + "endpoint",
        data = {"policy": POLICY_NAME_TO_ID[self.policy_name],  # policy id
                  "name": self.mooclet_name}
        headers = {'Authorization': f'Token {self.token}'}

        return _mooclet_api_call(url, data=data, headers=headers)


class MoocletConnector:

    def __init__(self, mooclet_id, token, url):
        self.token = token
        self.url = url
        self.mooclet_id = mooclet_id

        try:
            self.get_mooclet()
        except requests.HTTPError as e:
            raise e

    def _mooclet_get_call(self, endpoint, params=None, headers=None, url=None) -> Dict:
        if url == None:
            url = self.url + endpoint

        if params == None:
            params = {"mooclet": self.mooclet_id}

        if headers == None:
            headers = {'Authorization': f'Token {self.token}'}

        return _mooclet_api_call(url, params=params, headers=headers)

    def _mooclet_post_call(self, endpoint, data, headers=None, url=None) -> Dict:
        if url == None:
            url = self.url + endpoint

        if headers == None:
            headers = {'Authorization': f'Token {self.token}'}

        return _mooclet_api_call(url, data=data, headers=headers)

    def get_mooclet(self) -> Dict:
        url = self.url + "mooclet/" + str(self.mooclet_id)
        return self._mooclet_get_call("mooclet", url=url)

    def get_versions(self) -> Dict:
        return self._mooclet_get_call("version-name")

    def get_policy_parameters(self) -> Dict:
        return self._mooclet_get_call("policyparameters")
    

    def create_policy_parameters(self, policy_id: int, parameters: Dict) -> Dict:
        data = {
            "mooclet": self.mooclet_id,
            "policy": policy_id,
            "parameters": parameters
        }

        return self._mooclet_post_call("policyparameters", data=data)

    """
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
    """

    def get_values(self) -> Dict:
        return self._mooclet_get_call("value")

    def get_policy_parameters_history(self) -> Dict:
        return self._mooclet_get_call("policyparametershistory")
    
#mooclet = MoocletConnector(25)

# new_mooclet_id = mooclet.create_mooclet("301 " + str(datetime.datetime.now()), 
#                                         "thompson_sampling_contextual")
# mooclet.get_mooclet(new_mooclet_id)
