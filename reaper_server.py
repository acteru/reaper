#!/usr/bin/env python

import yaml
import os
import sys
import subprocess
import errno
import platform

from optparse import OptionParser


class reaper:


    def parse_commands(self):
        parser = OptionParser(usage="usage: %prog [options] repository",
                              version="%prog 1.0")
        parser.add_option("-s","--status",
                          help="show current repository state")
        parser.add_option("-X","--sync",
                          help="syncs all clients to master")
        parser.add_option("-b","--background",
                          help="runs reaper in background")
        parser.add_option("-i","--add-instance",
                          help="add's new mastere instance")
        (option,args) = parser.parse_args()

        if len(args) != 1:
            parser.error("wrong number of arguments")
        print option
        print args


    def check_platform(self):
        os = platform.linux_distribution()
        if "Fedora" in os[0]:
            packagemanager = "dnf"
        elif "Centos" in os[0]:
            packagemanager = "yum"
        elif "CentOS Linux" in os[0]:
            packagemanager = "yum"
        elif "RedHat" in os[0]:
            packagemanager = "yum"
        else:
            print ("Your Operatingsystem is not supported please use CentOS, RHEL or Fedora")
            sys.exit()
        return(packagemanager)


    # show the current status of synced repositories
    def print_status(self):
        print "Print current synced repositories"


    # sync repository or repositories
    def sync_client(self,loaded_config):
        syncClient = "rsync copy and mirror "
        try:
            subprocess.check()
        except:
            print ("rsync not found --try yum install rsync")


    # sync all clients --default behavior
    def sync_all_clients(self):
        for i in reaper.clients:
            print i


    def add_instance(self):
        print "add new instance"


    # create folders for the reaper class
    def create_dir(self,path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    # load config
    def load_config(self):
        with open('config/master_config.yaml', 'r') as config_load:
            try:
                loaded_config = yaml.load(config_load)
                return loaded_config
            except yaml.YAMLError as exc:
                print exc


if __name__ == "__main__":
    try:
        reaper = reaper()
        (option,args) = reaper.parse_commands()

    except KeyboardInterrupt:
        sys.exit(0)