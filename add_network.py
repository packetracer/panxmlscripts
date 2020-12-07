#!/env/python3
import json
import requests
from jinja2 import Template
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

key = 'LUFRPT1wVlIxZVB1V0FrNjdoTHRGcy9NZndQanNLT3M9WDVSNUFyV05wZnZETjh3L2d6Wkx4dUttQjFlN2J5K2FWYjV0bzVYY2lxTDR0emxsMjVPY21sR3NxUGpjRDVCeg=='
ip = '192.168.1.48'
FILENAME = 'test.json'


def open_json_file():
    with open(FILENAME) as f:
        data = json.load(f)
    f.close()
    return data

def send_obj(obj_name,CIDR):
    tp = Template("https://{{ ip }}/api/?key={{ key }}&type=config&action=set&xpath=/config/shared/address/entry[@name='{{ obj_name }}'] &element=<ip-netmask>{{ CIDR }}</ip-netmask>")
    msg = tp.render(ip=ip, key=key, obj_name=obj_name, CIDR=CIDR)
    s = requests.session()
    s.verify=False
    r = s.get(msg)
    print(r.text)

def netmask_to_cidr(netmask):
    '''
    :I stole this function from the internet. 
    :param netmask: netmask ip addr (eg: 255.255.255.0)
    :return: equivalent cidr number to given netmask ip (eg: 24)
    '''
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

data = open_json_file()
for (k,v) in data.items():
    CIDR = (v['IP'])+ ('/'+str(netmask_to_cidr(v['Netmask'])))
    send_obj(v['Name'], CIDR)
