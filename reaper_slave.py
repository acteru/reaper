#!/usr/bin/python3

#TODO add import logging
import subprocess
import sys
import argparse
import yaml

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
                self.os = config["operatingsystem"]
                self.repositories = config["repositories"]
                self.repository_data_path = config["repository_data_path"]
                self.reaper_master = config["reaper_master"]
                self.os_major_v = config["osmajorversion"]
                self.remote_user = config["remote_user"]
            except:
                print(yaml.YAMLError)

class Repositories():
    """ Used to get new packages from upstream repositories
    and pushing< repositories to reaper master """
    def get_upstream_packages(self):
        """get all packages from the upstream repositories"""
        s_cnf = Config()
        for repo in s_cnf.repositories:
            cmd = "reposync -p {1} -r {2}".format(s_cnf.repository_data_path, repo)
            print(cmd)
            subprocess.check_output(cmd, shell=True)

    def push_to_master(self):
        """Create folders on master and push new Packages to the reaper master"""
        s_cnf = Config()
        cmd_folder = "ssh {0}@{1} 'mkdir -p /var/repo/{2}/{3}'".format(s_cnf.remote_user, s_cnf.reaper_master, s_cnf.os, s_cnf.os_major_v)
        cmd = "rsync -a {0} {1}:/var/repo/{2}/{3}".format(s_cnf.repository_data_path, s_cnf.reaper_master, s_cnf.os, s_cnf.os_major_v)
        print(cmd)
        subprocess.check_output(cmd_folder, shell=True)
        subprocess.check_output(cmd, shell=True)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='trigger reaper functions')
    parser.add_argument('-x', '--sync', action='store_true', help="get upstream repositories")
    parser.add_argument('-p', '--push', action='store_true', help="push repositories to master")
    args = vars(parser.parse_args())
    if len(args) == 1:
        parser.print_help()
        sys.exit(1)
    elif args['sync'] == True:
        r = Repositories()
        r.get_upstream_packages()
    elif args['push'] == True:
        r = Repositories()
        r.push_to_master()