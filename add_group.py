#!/env/python3
import json
import requests
from jinja2 import Template
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

key = 'LUFRPT1wVlIxZVB1V0FrNjdoTHRGcy9NZndQanNLT3M9WDVSNUFyV05wZnZETjh3L2d6Wkx4dUttQjFlN2J5K2FWYjV0bzVYY2lxTDR0emxsMjVPY21sR3NxUGpjRDVCeg=='
ip = '192.168.1.48'
FILENAME = 'groups.json'


def open_json_file():
    with open(FILENAME) as f:
        data = json.load(f)
    f.close()
    return data

def send_obj(grpName,grpMembers):
    tp = Template("https://{{ ip }}/api/?key={{ key }}&type=config&action=set&xpath=/config/shared/address-group/entry[@name='{{ grpName }}']/static &element={{ grpMembers }}")
    msg = tp.render(ip=ip,key=key,grpName=grpName,grpMembers=grpMembers)
    print(msg)
    s = requests.session()
    s.verify=False
    r = s.get(msg)
    print(r.text)


data = open_json_file()
for (k,v) in data.items():
    for i in v:
        members = ""
        for item in i['MemberList']:
            members+=("<member>"+item+"</member>")
        send_obj(i['Name'],members)
