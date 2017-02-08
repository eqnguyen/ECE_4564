#!/usr/bin/python

# To explore what the W|A api call returns go to:
# http://products.wolframalpha.com/api/explorer/

import urllib
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

class wolfram(object):
    def __init__(self, appid):
        self.appID = appid;
        self.base_url = 'http://api.wolframalpha.com/v2/query?'

    def _get_xml(self, ip):
        # Retrieves only the plain text answers
        url_params = {'input': ip, 'format': "plaintext", 'appid': self.appID}

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
        return url.read()

    def search(self, ip):
        xml = self._get_xml(ip)

        root = ET.fromstring(xml)

        answers = []

        for pod in root.findall('pod'):
            answers.append(pod.find('subpod').find('plaintext').text)

        return answers
