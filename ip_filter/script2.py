# coding: utf-8

import sys
sys.path.append('/home/dharal1/forcepoint/')    # path to config.py file
from config import api_url, api_key, api_version, api_port        # for SMC API access
from smc import session           # for SMC API login logout
from smc.elements.network import IPList  # for manipulate IPList on SMC API

from time import sleep
import requests     # for make http request
import logging      # for debugging

# debugging
logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s.%(funcName)s: %(message)s')

# external public sources where find IP address to blacklist
EXTERNAL_SOURCES = [
    "external_source_1_exemple",        # external source url exemple 1
    "external_source_2_exemple"         # external source url exemple 2
    ]


def upload_as_json(name, mylist):
    """
    Upload the IPList as json payload.
    """
    location = list(IPList.objects.filter(name))
    if location:
        iplist = location[0]
        return iplist.upload(json=mylist, as_type="json")


def download_as_json(name):
    """
    Download IPList as json.
    """
    location = list(IPList.objects.filter(name))
    if location:
        iplist = location[0]
        return iplist.download(as_type="json")


def update_ip_list():
    """
    Update an list of IP address to blacklist.
    """
    # login to session SMC API Forcepoint
    session.login(url=api_url() + ":" + api_port(),     # IP address of SMC API
                  api_key=api_key(),    # API key to login session
                  api_version=api_version(),    # version of API
                  verify=False)         # no certificate needed

    ip_list = []    # IP address list to update on Forcepoint

    for external_source in EXTERNAL_SOURCES:
        # collect IP address for each external public source
        req = requests.get(external_source)
        # init IP address list for each source
        src_list = req.text.replace('\n', '\r')
        src_list = src_list.split('\r')
        for ip_domain in src_list:  # for each IP address
            # get differents parts of the address
            values = ip_domain.split('.')
            is_ip = False
            if len(values) == 4:
                index = 0   # number of part of the address
                while index < 4:
                    # verify if each part of the address is a number
                    if values[index].isnumeric():
                        is_ip = True
                    else:
                        is_ip = False
                        break
                    index += 1
            if is_ip:
                # init IP address list from all sources
                ip_list.append(str(ip_domain))

    # update the IP list
    upload_as_json('test_iplist', {'ip': ip_list})  # update address list 

    session.logout()  # logout session


if __name__ == "__main__":
    while True:
        update_ip_list()
        sleep(60)  # update every 1 min
