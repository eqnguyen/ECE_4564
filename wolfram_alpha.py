#!/usr/bin/python

# To explore what the W|A api call returns go to:
# http://products.wolframalpha.com/api/explorer/

import urllib
import json
from urllib.request import Request, urlopen

class wolfram(object):
    def __init__(self, appid):
        self.appID = appid;
        self.base_url = 'http://api.wolframalpha.com/v2/query?'

    def _get_json(self, ip):
        # Retrieves only the plain text answers and formats the stuff returned by the api call using JSON
        url_params = {'input': ip, 'format': "plaintext", 'output': "JSON", 'appid': self.appID}

        # encodes the parameters
        data = urllib.parse.urlencode(url_params).encode()

        # creates a request with the base url and encoded parameters
        req = Request(self.base_url, data)

        try:
            # get and return the json
            url = urlopen(req)
        except IOError:
            print("IO ERROR")
            return "{}"

        # read gives a byte stream, decode makes a string
        return url.read().decode()

    def search(self, ip):
        answerjson = self._get_json(ip)

        # TODO get the relevant information from the json

        answer = json.loads(answerjson)

        return answerjson
