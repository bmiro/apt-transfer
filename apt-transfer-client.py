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

## IMPORTANT TODO: catch kill singals and recover sources before exiting

import sys.argv
import shlex.split
import shutil.copy
import datetime.date
import urllib.request
import subprocess.Popen

# Names of the files to donwload from the apt-transfer-server
PACKAGE_LIST_NAME_URL = "package.list"
SOURCES_LIST_NAME_URL = "sources.list"

# Paths of the local sources.list files
SOURCES_LIST_FILE = "/etc/apt/sources.list"
SOURCES_LIST_BACKUP_FILE = "/etc/apt/sources.list.bak"


def print_help():
    print("apt-transfer-client server_url \n \
\t i.e.: apt-transfer-client 192.168.254.1/apt-transfer.")


def override_sources_list(server_url):
    # Sources list backup
    SOURCES_LIST_BACKUP_FILE += str(datetime.date.today())
    print("Saving a backup of sources.list to " + SOURCES_LIST_BACKUP_FILE)
    shutil.copy(SOURCES_LIST_FILE, SOURCES_LIST_BACKUP_FILE)
    
    # Retriving the new sources.list
    server_url += "/" + SOURCES_LIST_NAME
    print("Retriving sources list file from the server " + server_url + "...")
    new_sourceslist_url = urllib.request.urlopen(server_url)
    new_sourceslist = new_sourceslist_url.read()

    # Overwritting the new sources list to the file
    sourceslist_file = open(SOURCES_LIST_FILE, "w")
    sourceslist_file.write(new_sourceslist)
    sourceslist_file.close()

    apt_get_update_args = shlex.split("apt-get update")
    apt_get_update = subprocess.Popen(apt_get_update_args)
    apt_get_update.wait()


def recover_sources_list():
    shutil.copy(SOURCES_LIST_BACKUP_FILE, SOURCES_LIST_FILE)


def parse_package_list(package_list):
    packages = package_list.decode('utf-8') 
    packages.replace("\n", " ")
    return packages


def get_package_list(server_url):
    server_url += "/" + PACKAGE_LIST_NAME
    print("Retriving package list from " + server_url + "...")
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


