import requests
from typing import Dict, List
from commons.exceptions import ServiceUnavailable, ProxyAuthenticationRequired, ExternalResourceNotFound
import os
from django.conf import settings

# never use this token to perform any Delete requests
# never use the token outside of this file
DUMMY_MOOCLET_API_TOKEN = os.getenv("DUMMY_MOOCLET_API_TOKEN")
DUMMY_MOOCLET_URL = settings.DEFAULT_MOOCLET_URL

POLICY_NAME_TO_ID = {"thompson_sampling_contextual": 6,
                     "choose_policy_group": 12,
                     "ts_configurable": 17}

def mooclet_call(method, **kwargs):
    try:
        response = method(**kwargs)
    except requests.exceptions.ConnectionError as e:
        raise ServiceUnavailable(detail='Service unavailable, check your url or try again later.')

    status_code = response.status_code

    if status_code == 401:
        raise ProxyAuthenticationRequired()
    if status_code == 404:
        print(kwargs)
        raise ExternalResourceNotFound('That mooclet does not exist on the external server')

    response.raise_for_status()

    return response

class ExternalServerConnector:
    def __init__(self, token, url):
        self.token = token
        self.url = url
        # Probably should use library for joining urls, but don't have time to learn that
        if self.url[-1] != "/":
            self.url = self.url + "/"

    def get_authorization_header(self):
        return {'Authorization': f'Token {self.token}'}

    def check_server(self):
        url = self.url
        headers = {'Authorization': f'Token {self.token}'}

        kwargs = {'url': url, 'headers': headers}
        response = mooclet_call(requests.head, **kwargs)
        return response


class MoocletCreator(ExternalServerConnector):
    def __init__(self, token, url, mooclet_name, policy_name):
        super().__init__(token=token, url=url)
        self.mooclet_name = mooclet_name
        self.policy_name = policy_name

    def create_mooclet(self) -> Dict:
        endpoint = "mooclet"
        url = self.url + endpoint,

        data = {"policy": POLICY_NAME_TO_ID[self.policy_name],  # policy id
                  "name": self.mooclet_name}
        headers = self.get_authorization_header()

        kwargs = {'url': url, 'data': data, 'headers': headers}

        #results = _mooclet_get_call(url, params=params, headers=headers)
        response = mooclet_call(requests.post, **kwargs)
        return response.json()


class MoocletConnector(ExternalServerConnector):
    def __init__(self, mooclet_id, token, url):
        super().__init__(token=token, url=url)

        self.mooclet_id = mooclet_id


    def _mooclet_get_call(self, endpoint, params=None, headers=None, url=None) -> Dict:
        if url == None:
            url = self.url + endpoint

        if params == None:
            params = {"mooclet": self.mooclet_id}

        if headers == None:
            headers = self.get_authorization_header()

        kwargs = {'url': url, 'params': params, 'headers': headers}

        #results = _mooclet_get_call(url, params=params, headers=headers)
        response = mooclet_call(requests.get, **kwargs)
        results = response.json()

        page = results

        while ("next" in page.keys() and page["next"] != None):
            kwargs['url'] = results['next']
            page = mooclet_call(requests.get, **kwargs).json()
            results["results"] += page["results"]

        return results


    def _mooclet_post_call(self, endpoint, data, headers=None, url=None) -> Dict:
        if url == None:
            url = self.url + endpoint

        if headers == None:
            headers = self.get_authorization_header()

        kwargs = {'url': url, 'data': data, 'headers': headers}

        #results = _mooclet_get_call(url, params=params, headers=headers)
        response = mooclet_call(requests.post, **kwargs)
        return response.json()

    def check_mooclet(self):
        url = self.url + "mooclet"
        params = {"mooclet": self.mooclet_id}
        headers = self.get_authorization_header()

        kwargs = {'url': url, 'params': params, 'headers': headers}
        response = mooclet_call(requests.head, **kwargs)

        return response

    def get_mooclet(self, fields: List[str]=None):
        url = self.url + "mooclet/" + str(self.mooclet_id)
        data = self._mooclet_get_call("mooclet", url=url)

        if not fields:
            return data

        ret = {}

        for field in fields:
            ret[field] = data[field]

        return ret

    def get_versions(self) -> Dict:
        return self._mooclet_get_call("version")

    def create_versions(self, version_name: str, version_json: str, version_text: str) -> Dict:
        data = {
            "mooclet": self.mooclet_id,
            "name": version_name,
            "version_json": version_json,
            "text": version_text
        }

        return self._mooclet_post_call("version", data=data)

    def get_policy_parameters(self) -> Dict:
        return self._mooclet_get_call("policyparameters")

    def create_policy_parameters(self, policy_id: int, policy_parameters: str) -> Dict:
        data = {
            "mooclet": self.mooclet_id,
            "policy": policy_id,
            "parameters": policy_parameters
        }
        return self._mooclet_post_call("policyparameters", data=data)

    def get_values(self) -> Dict:  # for getting variable values
        return self._mooclet_get_call("value")

    def create_value(self, variable_name):
        data = {
            "variable": variable_name,
            "mooclet": self.mooclet_id
        }
        return self._mooclet_post_call("value", data=data)

    def create_variable(self, variable_name: str) -> Dict:
        data = {"name": variable_name}
        return self._mooclet_post_call("variable", data=data)

    def get_policy_parameters_history(self) -> Dict:
        return self._mooclet_get_call("policyparametershistory")
