#!/env/python3
import json
import requests
from jinja2 import Template
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

key = '<KEY>'
ip = '1.1.1.1'
FILENAME = 'groups.json'


def open_json_file():
    with open(FILENAME) as f:
        data = json.load(f)
    f.close()
    return data

def send_obj(grpName,grpMembers):
    tp = Template("https://{{ ip }}/api/?key={{ key }}&type=config&action=set&xpath=/config/shared/address-group/entry[@name='{{ grpName }}']/static &element={{ grpMembers }}")
    msg = tp.render(ip=ip,key=key,grpName=grpName,grpMembers=grpMembers)
    s = requests.session()
    s.verify=False
    r = s.get(msg)

data = open_json_file()
for (k,v) in data.items():
    for i in v:
        members = ""
        for item in i['MemberList']:
            members+=("<member>"+item+"</member>")
        send_obj(i['Name'],members)
