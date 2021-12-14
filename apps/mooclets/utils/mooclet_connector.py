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
    url = kwargs["url"]
    headers = kwargs["headers"]

    try:
        response = method(**kwargs)
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailable(detail='Service unavailable, check your url or try again later.')

    status_code = response.status_code

    if status_code == 401:
        raise ProxyAuthenticationRequired()
    if status_code == 404:
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
        # Could use check_server, but not doing it here to reduce number of external calls

    def get_authorization_header(self):
        return {'Authorization': f'Token {self.token}'}

    def check_server(self):
        url = self.url
        headers = self.get_authorization_header()

        kwargs = {'url': url, 'headers': headers}
        response = mooclet_call(requests.head, **kwargs)

        return response

class MoocletCreator(ExternalServerConnector):
    def __init__(self, token, url):
        super().__init__(token=token, url=url)

    def create_mooclet(self, name: str, policy: int):
        url = self.url + "mooclet"

        data = {"policy": policy,  # policy id
                  "name": name}

        headers = self.get_authorization_header()
        timeout = 20

        kwargs = {'url': url, 'data': data, 'headers': headers, 'timeout': timeout}

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

        response = mooclet_call(requests.get, **kwargs)
        response_json = response.json()

        page = response_json

        while ("next" in page.keys() and page["next"] != None):
            kwargs['url'] = page['next']
            page = mooclet_call(requests.get, **kwargs).json()
            response_json["results"] += page["results"]

        return response_json


    def _mooclet_post_call(self, endpoint, data, headers=None, url=None):
        if url == None:
            url = self.url + endpoint

        if headers == None:
            headers = self.get_authorization_header()

        kwargs = {'url': url, 'data': data, 'headers': headers}

        response = mooclet_call(requests.post, **kwargs)

        response_json = response.json()

        page = response_json

        while ("next" in page.keys() and page["next"] != None):
            kwargs['url'] = page['next']
            page = mooclet_call(requests.get, **kwargs).json()
            response_json["results"] += page["results"]

        return response_json

    def check_mooclet(self):
        url = self.url + "mooclet"
        params = {"mooclet": self.mooclet_id}
        headers = self.get_authorization_header()

        kwargs = {'url': url, 'params': params, 'headers': headers}
        response = mooclet_call(requests.head, **kwargs)

        return response.status_code == 200

    def get_mooclet(self, fields: List[str]=None):
        endpoint = "mooclet/" + str(self.mooclet_id)
        data = self._mooclet_get_call(endpoint=endpoint)

        if not fields:
            return data

        ret = {}

        for field in fields:
            ret[field] = data[field]

        return ret

    def get_versions(self):
        return self._mooclet_get_call("version")

    def get_policy_parameters(self):
        return self._mooclet_get_call("policyparameters")

    def get_policy_parameters_history(self):
        return self._mooclet_get_call("policyparametershistory")

    def get_values(self):  # for getting variable values
        return self._mooclet_get_call("value")

    def get_policies(self):
        return self._mooclet_get_call("policy")

    def get_learner(self, learner_id: int):
        return self._mooclet_get_call("learner/" + str(learner_id))

    def create_versions(self, **data):
        data["mooclet"] = self.mooclet_id
        return self._mooclet_post_call("version", data=data)


    def create_policy_parameters(self, **data):
        data["mooclet"] = self.mooclet_id
        return self._mooclet_post_call("policyparameters", data=data)


    def create_value(self, variable_name):
        data = {
            "variable": variable_name,
            "mooclet": self.mooclet_id
        }
        return self._mooclet_post_call("value", data=data)

    def create_variable(self, **data):
        return self._mooclet_post_call("variable", data=data)

