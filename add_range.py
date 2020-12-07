#!/env/python3
import json
import requests
from jinja2 import Template
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

key = '<KEY>'
ip = '1.1.1.1'
FILENAME = 'ranges.json'

def open_json_file():
    with open(FILENAME) as f:
        data = json.load(f)
    f.close()
    return data

def send_obj(obj_name,rng):
    tp = Template("https://{{ ip }}/api/?key={{ key }}&type=config&action=set&xpath=/config/shared/address/entry[@name='{{ obj_name }}'] &element=<ip-range>{{ rng }}</ip-range>")
    msg = tp.render(ip=ip, key=key, obj_name=obj_name, rng=rng)
    s = requests.session()
    s.verify=False
    r = s.get(msg)


data = open_json_file()

for (k,v) in data.items():
    for j in v:
        send_obj(v[j]['Name'],v[j]['IPStart']+'-'+v[j]['IPEnd'])
