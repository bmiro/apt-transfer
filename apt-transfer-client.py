#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##########################################################################
#   This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
#   This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
##########################################################################


import sys
import shlex
import subprocess
import urllib.request

PACKAGE_LIST_NAME = "package.list"
SOURCES_LIST_BACKUP_NAME = "sources.list.apt-transfer.bak"
SOURCES_LIST_PATH = "/etc/apt"

def print_help():
    print("apt-transfer-client server_url \n \
\t i.e.: apt-transfer-client 192.168.254.1/apt-transfer.")

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


