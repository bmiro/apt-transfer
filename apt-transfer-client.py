#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import shlex
import subprocess
import urllib.request

usage_text = "apt-transfer-client server_url \n \
\t i.e.: apt-transfer-client 192.168.254.1/apt-transfer.\n"

PACKAGE_LIST_NAME = "package.list"
SOURCES_LIST_BACKUP_NAME = "sources.list.apt-transfer.bak"

def override_sources_list(server_url):
    pass 


def recover_sources_list():
    pass


def parse_package_list(package_list):
    packages = package_list.decode('utf-8') 
    return packages


def get_package_list(server_url):
    server_url += "/" + PACKAGE_LIST_NAME
    print("\nRetriving package list from " + server_url + "...")
    package_list_url = urllib.request.urlopen(server_url)
    package_list = package_list_url.read()
    return package_list


def install_packages(package_list):
    print("Launching apt-get tool")
    apt_get_install_args = shlex.split("apt-get install -y " + package_list)
    apt_get_install = subprocess.Popen(apt_get_install_args)
    apt_get_install.wait()


if __name__=='__main__':
    if len(sys.argv) < 2:
        print(usage_text)
        exit()
    
    server_url = sys.argv[1]

    package_list = get_package_list(server_url)
    packages = parse_package_list(package_list)
    override_sources_list(server_url)
    install_packages(packages)
    recover_sources_list()


