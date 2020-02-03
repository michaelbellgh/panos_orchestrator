import requests, os
import xml.etree.ElementTree as ET
from requests.utils import quote

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PanClient:

    params = {
        'hostname' : ''
    }

    options = {
        'verify_certs' : False,
        'https_port' : 443
    }

    api_key = ''

    system_info = {}

    error_dict = {
    '400' : 'Bad request',
    '403' : 'Forbidden',
    '1' : 'Unknown command',
    '2' : 'Internal error',
    '3' : 'Internal error',
    '4' : 'Internal error',
    '5' : 'Internal error',
    '6' : 'Bad Xpath',
    '7' : 'Object not present',
    '8' : 'Object not unique',
    '10' : 'Reference count not zero',
    '11' : 'Internal error',
    '12' : 'Invalid object',
    '14' : 'Operation not possible',
    '15' : 'Operation denied',
    '16' : 'Unauthorized',
    '17' : 'Invalid command',
    '18' : 'Malformed command',
    '19' : 'Success',
    '20' : 'Success',
    '21' : 'Internal error',
    '22' : 'Session timed out'}

    def log_error(self, error, level):
        print("[" + level + "]: " + error)

    def construct_api_url(self, cmd_type, cmd):
        hostname = self.params['hostname'] 
        key = self.api_key
        port = self.options['port']
        
        url = F"https://{hostname}:{port}/api/?key={key}&type={cmd_type}&cmd={cmd}"
        return url

    def get_api_key(self, username, password):
        hostname = self.params['hostname']
        port = self.options['https_port']
        url = F"https://{hostname}:{port}/api/?type=keygen&user={username}&password={password}"

        response = requests.get(url, verify=self.options['validate_certs'])
        root = ET.fromstring(response.text)
        key = root.find('result/key')

        if key is not None:
            return key.text
        else:
            self.log_error("Invalid credentials / API key not found", "ERROR")
            return None

    def populate_system_info(self):


    def __init__(self, hostname, username, password, verify_certs=False, https_port=443):
        self.params['hostname'] = hostname
        self.options['https_port'] = https_port
        self.options['validate_certs'] = verify_certs

        self.api_key = self.get_api_key(username, password)
        


pc = PanClient('palo', 'admin', 'FY*bXcz6ws5yrq')
print(pc.api_key)
