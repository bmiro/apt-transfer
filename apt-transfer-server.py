#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import shlex
import shutil
import os.path
import subprocess

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

SOURCES_ARCHES=["amd64", "armel", "i386", "ia64", "kfreebsd-amd64", "kfreebsd-i386", \
"mips", "mipsel", "powerpc", "s390", "sparc"]

COMMAND_LIST = ["mirror", "initialize", "update", "start", "stop", "clean"]

# TODO a nicer way to configure, maybe conffile
MIRROR_PATH = "/tmp/apt-mirror" #TODO! change this
MIRROR_LIST_PATH = "/etc/apt/mirror.list"
MIRROR_LIST_TEMPLATE_PATH = "./mirror-template.list"

WWW_PATH = "/var/www/apt-transfer"

SOURCES_LIST_PATH = "/etc/apt/sources.list"
SOURCES_LIST_WWW_PATH = WWW_PATH + "/sources.list"
PACKAGE_LIST_WWW_PATH = WWW_PATH + "/packages.list"
MIRROR_WWW_PATH = WWW_PATH + "/apt-mirror"
HTACCESS_WWW_PATH = WWW_PATH + "/.htaccess"

HTACCESS_DENY = "#deny all access\ndeny from all\n"

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
    # command ARCH        URL                 VERSION SECTIONS    (optional) PATH
    # mirror i386 http://ftp.debian.org/debian/ sid main contrib --dest-path /tmp
    if command == "mirror":

        #ARCH
        idx = 2
        if len(arg_v) < idx+1:
            return {"error" : "Architecture missing"}
        
        arch = arg_v[idx] #2
        if not arch in SOURCES_ARCHES:
            return {"error" : "The architecture %s is not recognized." % (arch)}
        
        arg["arch"] = arch
        idx +=1
        
        #URL
        url = arg_v[idx] #3
        if not validate_url(url):
            return {"error" : "I don't understand the mirror url " + url}

        arg["url"] = url
        idx += 1 

        #VERSION
        if len(arg_v) < idx+1:
            return {"error" : "Version missing"}

        version = arg_v[idx] #4
        if not version in SOURCES_VERSIONS:
            return {"error" : "I don't understand the version " + version}

        arg["version"] = version
        idx += 1

        #SECTIONS
        sections = []
        while idx < len(arg_v) and arg_v[idx] in SOURCES_SECTIONS:
            sections.append(arg_v[idx])
            idx += 1
        #Here the i points to --dest-path if exist

        if not sections:
            return {"error" : "I don't detect any software section (ie main)"}

        if arg_v[idx-1] != "--dest-path" and not arg_v[idx-1] in SOURCES_SECTIONS:
            return {"error" : "I don't understand the section " + arg_v[idx]}

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

    if command == "start":
        #Interface
        idx = 2
        if len(arg_v) < idx+1:
            return {"error" : "You need to specify server's network interface."}
        
        arg["interface"] = arg_v[idx] #2
        
    return arg


""" How to see if si a valid repo url? so hard..."""
def validate_url(url):
    return True


""" creates a mirror of the given repository to the given path 
" It may need many space
"""
def mirror(arch, url, version, sections):

    # Generate the mirror.list for apt-mirror
    mirror_template_file = open(MIRROR_LIST_TEMPLATE_PATH, "r") 
    mirror_template = mirror_template_file.read()
    mirror_template_file.close()

    mirror_template = mirror_template.replace("ARCH", arch)
    mirror_template = mirror_template.replace("URL", url)
    mirror_template = mirror_template.replace("VERSION", version)

    sects = ""
    for section in sections:
        sects += section + " "

    mirror_template = mirror_template.replace("SECTIONS", sects)
    mirror_template = mirror_template.replace("PATH", MIRROR_PATH)
    

    # Copy mirror-list to apt-mirror conf folder
    mirror_file = open(MIRROR_LIST_PATH, "w")
    mirror_file.write(mirror_template)
    mirror_file.close()

    # Create mirror directory
    if not os.path.isdir(MIRROR_PATH):
        os.mkdir(MIRROR_PATH)

    # Create apt-transfer direcotry in WWW
    if not os.path.isdir(WWW_PATH):
        os.mkdir(WWW_PATH)

    # Executing apt-mirror
    apt_mirror_cmd = shlex.split("apt-mirror")
    apt_mirror = subprocess.Popen(apt_mirror_cmd)
    apt_mirror.wait()

    mirror_path = MIRROR_PATH + "/mirror"

    # Mirror creates a dir structure and the real mirror is 2 levels inside
    # Subdir 1 contains name of the server mirrored
    subdir = os.listdir(mirror_path)[0]
    mirror_path += "/" + subdir
    # Subdir 1 contains the distro name, debian or ubuntu
    distro = os.listdir(mirror_path)[0]
    mirror_path += "/" + distro
    
    # Create mirror directory in www-server
    if not os.path.isdir(MIRROR_WWW_PATH):
        os.mkdir(MIRROR_WWW_PATH)

    # Create symlink to www-server direcory
    mirror_www_path = MIRROR_WWW_PATH + "/" + distro
    if not os.path.islink(mirror_www_path) and \
       not os.path.isdir(mirror_www_path):
        os.symlink(mirror_path, mirror_www_path)


# Maybe this can be replaced by packages dependeces once a deb
# of this program is generated.
def install_needed_dependeces():
    pass


def initialize():
    pass
    
""" Returns the ip of the given interface or false if any problem """ 
def check_network_interface(interface):
    ifconfig_cmd = shlex.split("ifconfig " + interface)
    ifconfig_exec = subprocess.Popen(ifconfig_cmd, stdout=subprocess.PIPE)
    ifconfig = ifconfig_exec.stdout.read()

    addr_search = re.search(r"inet addr:([0-9.]+)\s+Bcast", ifconfig)
    if addr_search:
        return addr_search.group(1)
    else:
        return False

    #TODO i'm here test this function



""" Starts serving the apt-transfer-server to the given path (must be accessible 
" to the webserver """
def start(interface):

    interface_address = check_network_interface(interface)    
    if not interface_address:
        print("Network intarface %s doesn't exist or is not ready to use." \
              % (interface)}
        return

    #List system packages to create the list
    dpkg_l_cmd = shlex.split("dpkg -l")
    dpkg_l = subprocess.Popen(dpkg_l_cmd, stdout=subprocess.PIPE)
    raw_package_list = dpkg_l.stdout.read()    
   
    package_list = []
    for package_line in raw_package_list.split("\n"):
        if package_line[0:2] == "ii": # Means that is a installed package 
            package_name = package_line.split(" ")[2]
            package_list.append(package_name)

    #Creates the folder visible to the webserver if not created before
    if not os.path.isdir(WWW_PATH):
        os.mkdir(WWW_PATH)

    #Write the package list to a file
    package_list_file = open(PACKAGE_LIST_WWW_PATH, "w")
    for package in package_list:
        package_list_file.write(package)
        package_list_file.write("\n")

    package_list_file.close()

    # Writes sources.list that will be given to the client
    
    # Check if the mirror is created sources list, if not give the system one.
    if os.path.isdir(MIRROR_WWW_PATH):
        sources_list = open(SOURCES_LIST_WWW_PATH, "w")
        sources_list.write("hola nene\n")
        sources_list.close()
    else:
        # We are not a mirror, we will give our sources.list to the client
        shutil.copy(SOURCES_LIST_PATH, SOURCES_LIST_WWW_PATH)

    # Delete htaccess if exist that deny web access
    if os.path.isfile(HTACCESS_WWW_PATH):
        os.remove(HTACCESS_WWW_PATH)


""" Stops sharing the package.list and source.list setting a htaccess file."""
def stop():
    htaccess = open(HTACCESS_WWW_PATH, "w")
    htaccess.write(HTACCESS_DENY)
    htaccess.close() 


""" Clean all files and configurations of the program, also the mirror
" if is created
"""
def clean():
    if os.path.isdir(WWW_PATH):
        shutil.rmtree(WWW_PATH)

    if os.path.isdir(MIRROR_PATH):
        shutil.rmtree(MIRROR_PATH)

    if os.path.islink(MIRROR_WWW_PATH):
        shutil.rmtree(MIRROR_WWW_PATH)

if __name__=='__main__':

    arg = arg_parsing(sys.argv)

    if "error" in arg:
        if arg["error"] == "No command specified":
            print_help()
        else:    
            print(arg["error"])
    
        exit()

    if arg["command"] == "mirror":
        mirror(arg["arch"], arg["url"], arg["version"], arg["sections"])

    elif arg["command"] == "initialize":
        initialize()

    elif arg["command"] == "update":
        update(arg["url"], arg["distro"], arg["sections"])

    elif arg["command"] == "start":
        start(arg["interface"])

    elif arg["command"] == "stop":
        stop()

    elif arg["command"] == "clean":
        clean()
    
    else:
        print("Chuck Norris is dead.")

