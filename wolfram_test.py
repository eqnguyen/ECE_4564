#!/usr/bin/python

# To explore what the W|A api call returns go to:
# http://products.wolframalpha.com/api/explorer/

import urllib
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

        # get and return the json
        json = urlopen(req).read()
        return json

    def search(self, ip):
        json = self._get_json(ip)
        return json

# Thomas's appid
appID = '43UVWL-U3JYWWV895'

# Queries user for input
query = input("Enter your question: ")

# create a new instance of the wolfram class
w = wolfram(appID)

# just prints the json returned
print(w.search(query).decode())
