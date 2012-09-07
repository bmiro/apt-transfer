#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import shlex
import subprocess
import os.path

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



VERSION="pre-alpha"

SOURCES_VERSIONS=[# Debian
                 "oldstable", "stable", "testing", "unstable", "experimental",\
                 "buzz", "rex", "bo", "hamm", "slink", "potato","woody", \
                 "sarge", "etch", "lenny", "squeeze", "wheezy", "jessie",\
                 "sid",\
                 # Ubuntu
                 "warty", "hoary", "breezy", "dapper", "edgy", "feisty", \
                 "gutsy", "hardy", "intrepid", "jaunty", "karmic", \
                 "maverick", "lucid", "natty", "oneiric", "precise", "quantal"]

SOURCES_SECTIONS=["main", "contrib", "non-free",          # Debian
                  "universe", "multiverse", "restricted"] # Ubuntu specific

COMMAND_LIST = ["mirror", "initialize", "update", "start", "stop", "clean"]

DEFAULT_MIRROR_PATH="/var/www/apt-mirror"


def print_help():
    print("apt-transfer %s \n" % VERSION)
    print("Usage: apt-transfer-server command command-options\n")
    print("apt-transfer-server is a tool to share the list of installed \
packages on the \n machine and let another one with the apt-transfer-client to \
install them. \n It also can be used to create local mirrors of the debian-base \
repositories.\n")
    print("\nCommands:")
    print("\tmirror *source* - create a mirror of the given repository \
at the source with\n\t\t\tthe same sintax as sources.list to the given path.")
    print("\t\t[--dest-path *path*] - specify were the mirror will be stored")
    print("\tinitilize - prepare the system to start the service")
    print("\tupdate - updates the mirror packages")
    print("\tstart - start mirror server and allows access to packages list")
    print("\tstop - stop mirror server and denies access to packages list")
    print("\tclean - delete the full repository mirror")

    print("\nExamles:")
    #TODO put examples of each invocation


""" Argument parsing.
" @return: dict with command name and correspoding parameters depeding
" on which options has de command.
"""
def arg_parsing(arg_v):

    if len(arg_v) < 2:
        return {"error" : "No command specified"}
    
    command = arg_v[1]

    if not command in COMMAND_LIST:
        return {"error" : "I don't understand the command " + command}

    arg = {}
    arg["command"] = command

    # Mirror command has some special handling:
    # command        URL                 VERSION SECTIONS    (optional) PATH
    # mirror http://ftp.debian.org/debian/ sid main contrib --dest-path /tmp
    if command == "mirror":

        #COMMAND
        arg["command"] = "mirror"
        if len(arg_v) < 3:
            return {"error" : "URL missing"}

        #URL
        url = arg_v[2]
        if not validate_url(url):
            return {"error" : "I don't understand the mirror url " + url}

        arg["url"] = url 

        #VERSION
        if len(arg_v) < 4:
            return {"error" : "Version missing"}

        version = arg_v[3]
        if not version in SOURCES_VERSIONS:
            return {"error" : "I don't understand the version " + version}

        arg["version"] = version

        #SECTIONS
        sections = []
        i = 4 # The current index of the arg_v
        while i < len(arg_v) and arg_v[i] in SOURCES_SECTIONS:
            sections.append(arg_v[i])
            i += 1
        #Here the i points to --dest-path if exist

        if not sections:
            return {"error" : "I don't detect any software section (ie main)"}

        if arg_v[i-1] != "--dest-path" and not arg_v[i-1] in SOURCES_SECTIONS:
            return {"error" : "I don't understand the section " + arg_v[i]}

        arg["sections"] = sections
        
        #PATH
        if "--dest-path" in arg_v:
            idx = arg_v.index("--dest-path")
            if len(arg_v) < idx+2:
                return {"error" : "After --dest-path you must specify a path"}

            dest_path = arg_v[idx+1]

            if not os.path.isdir(dest_path):
                return {"error" : "The specified path doesn't exist " + dest_path}
        
            arg["path"] = dest_path

    return arg


def validate_url(url):
    return True


def mirror(url, version, sections, path):
    pass


# Maybe this can be replaced by packages dependeces once a deb
# of this program is generated.
def install_needed_dependeces():
    pass

def initialize():
    pass


def start():
    #List system packages
    dpkg_l_cmd = shlex.split("dpkg -l")
    dpkg_l = subprocess.Popen(dpkg_l_cmd, stdout=subprocess.PIPE)

    package_list = dpkg_l.stdout.read()

    print package_list

def stop():
    pass


def clean():
    pass


if __name__=='__main__':

    arg = arg_parsing(sys.argv)

    if "error" in arg:
        if arg["error"] == "No command specified":
            print_help()
        else:    
            print(arg["error"])
    
        exit()

    if arg["command"] == "mirror":
        if "path" in arg:
            path = arg["path"]
        else:
            path = DEFAULT_MIRROR_PATH
        mirror(arg["url"], arg["version"], arg["sections"], path)

    elif arg["command"] == "initialize":
        initialize()

    elif arg["command"] == "update":
        update(arg["url"], arg["distro"], arg["sections"])

    elif arg["command"] == "start":
        start()

    elif arg["command"] == "stop":
        stop()

    elif arg["command"] == "clean":
        clean()
    
    else:
        print("Chuck Norris is dead.")

