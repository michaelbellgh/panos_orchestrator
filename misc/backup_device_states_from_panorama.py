import requests
import xml.etree.ElementTree as ET

def get_api_key(hostname, username, password):
    url  = "https://" + hostname + "/api/?type=keygen&user=" + username + "&password=" + password
    response = requests.get(url,verify=False)
    root  = ET.fromstring(response.text)
    key = root.find('result/key')
    return key.text

def get_all_panorama_managed_ips(hostname, api_key, username=None, password=None):
    response = get_api_text(hostname, "type=op&cmd=<show><devices><connected></connected></devices></show>", api_key)
    root = ET.fromstring(response)
    ips = []
    for device in root.findall("result/devices/entry"):
        d = {}
        d["hostname"] = device.find("hostname").text
        d["ip"] = device.find("ip").text
        if username is not None and password is not None:
            d["api"] = get_api_key(d["hostname"], username, password)
        ips.append(d)
    return ips

def get_api_text(hostname, api_string, api_key):
    url = "https://" + hostname + "/api/?" + api_string + "&key=" + api_key
    return requests.get(url, verify=False).text

def get_api_data(hostname, api_string, api_key):
    url = "https://" + hostname + "/api/?" + api_string + "&key=" + api_key
    return requests.get(url, verify=False).content

def save_device_state(hostname, filename, api_key):
    content = get_api_data(hostname, "type=export&category=device-state", api_key)
    open(filename, mode="wb").write(content)

api = get_api_key("192.168.10.81", "admin", "admin")
ips = get_all_panorama_managed_ips("192.168.10.81", api, "admin", "admin")
for item in ips:
    save_device_state(item["ip"], item["hostname"], item["api"])
