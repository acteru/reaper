#!/usr/bin/env python

import yaml
import os
import sys
import subprocess
import errno
import platform
import argparse

class reaper:


    def parse_commands(self):
        parser = argparse.ArgumentParser(prog=sys.argv[0])
        parser.add_argument('-s','--status',help="show current repository state")
        parser.add_argument('-x','--sync',help="syncs all clients to master")
        parser.add_argument('-b','--background',help="runs reaper in background")
        parser.add_argument('-i','--add-instance',help="add's new mastere instance")
        args = parser.parse_args()

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
    def sync_client(self,client,client_path):
        rsync_cmd = "rsync -az reaper@%s:%s" % (client,client_path)
        try:
            subprocess.check_output(rsync_cmd, shell=True)
        except:
            print ("rsync not found --try yum install rsync")


    # sync all clients --default behavior
    def sync_all_clients(self,loaded_config):
        for i in loaded_config['sources']:
            reaper.sync_client(i,loaded_config['sources'][i]['path'])


    def add_instance(self):
        print "add new instance"


    # create folders for the reaper class
    def create_dir(self,path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


    # create user for reaper
    def create_user(self):
        try:
            useradd = "useradd reaper"
            subprocess.check_output(useradd, shell=True)
        except:
            print "wip"

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
        reaper.sync_all_clients(reaper.load_config())

    except KeyboardInterrupt:
        sys.exit(0)