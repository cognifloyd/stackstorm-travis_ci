from six.moves import http_client

import requests

from st2common.runners.base_action import Action

API_URL = 'https://api.travis-ci.org'
HEADER_ACCEPT = 'application/vnd.travis-ci.2+json'
HEADER_CONTENT_TYPE = 'application/json'


class TravisCI(Action):
    def _get_base_headers(self):
        headers = {}
        headers['Content-Type'] = HEADER_CONTENT_TYPE
        headers['Accept'] = HEADER_ACCEPT
        return headers

    def _get_auth_headers(self):
        headers = self._get_base_headers()
        headers['Authorization'] = 'token: "%s"' % (self.config['token'])
        return headers

    def _perform_request(self, path, method, data=None, requires_auth=False):
        url = API_URL + path

        if method == "GET":
            if requires_auth:
                headers = self._get_auth_headers()
            else:
                headers = {}
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            headers = self._get_auth_headers()
            response = requests.post(url, headers=headers)
        elif method == 'PUT':
            headers = self._get_auth_headers()
            response = requests.put(url, data=data, headers=headers)

        # pylint: disable=no-member
        if response.status_code in [http_client.FORBIDDEN, http_client.UNAUTHORIZED]:
            msg = ('Invalid or missing Travis CI auth token. Make sure you have'
                   'specified valid token in the config file')
            raise Exception(msg)

        return response
