#!/usr/bin/python3

#import logging
import subprocess
import sys
import argparse
import yaml

# cmd handler

class Config():
    """Loads yaml configuration file and deserialize the config"""
    def __init__(self):
        with open('slave_config.yml', 'r') as config_load:
            try:
                config = yaml.load(config_load)
                self.logfile_path = config["logfile_path"]
                self.loglevel_console = config["loglevel_console"]
                self.loglevel_file = config["loglevel_file"]
                self.packagemanager = config["packagemanager"]
                self.operatingsystem = config["operatingsystem"]
                self.repositories = config["repositories"]
                self.repository_data_path = config["repository_data_path"]
            except:
                print(yaml.YAMLError)

class Repositories():
    """ Used to get new packages from upstream repositories
    and pushing< repositories to reaper master """
    def get_upstream_packages(self):
        """get all packages from the upstream repositories"""
        slave_conf = Config()
        for repo in slave_conf.repositories:
            cmd = "{0} reposync -p {1} -r {2}".format(slave_conf.packagemanager, slave_conf.repository_data_path, repo)
            subprocess.check_output(cmd, shell=True)

    def push_to_master(self):
        """Push new Packages to the reaper master"""
        print("push packages with rsync to reaper master")


if __name__ == "__main__":
    
    ap = argparse.ArgumentParser(description='trigger reaper functions')
    ap.add_argument('-x', '--sync', action='store_true', help="get upstream repositories")
    ap.add_argument('-p', '--push', action='store_true', help="push repositories to master")
    args = vars(ap.parse_args())
    if args['sync'] == True:
        print("start sync")
    elif args['push'] == True:
        print("start push")