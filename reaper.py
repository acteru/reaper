#!/usr/bin/python3

import logging
import subprocess
import sys
import argparse
import yaml

class Config():
    """Loads yaml configuration file and deserialize the config"""
    def __init__(self):
        with open('./config.yaml', 'r') as config_load:
            try:
                config = yaml.load(config_load)
                self.logfile_path = config["logfile_path"]
                self.loglevel_console = config["loglevel_console"]
                self.loglevel_file = config["loglevel_file"]
                self.packagemanager = config["packagemanager"]
                self.os = config["operatingsystem"]
                self.os_major_v = config["os_major_version"]
                self.repositories = config["repositories"]
                self.repository_data_path = config["repository_data_path"]
                self.reaper_master = config["reaper_master"]
                self.remote_user = config["remote_user"]
                self.localhost_repository_data_path = "/srv/reaper/latest/{0}/{1}/".format(
                    self.os,
                    self.os_major_v
                )
            except:
                print(yaml.YAMLError)

class Repositories():
    """ Used to get new packages from upstream repositories
    and pushing< repositories to reaper master """
    def get_upstream_packages(self):
        """Get all packages from the upstream repositories"""
        if conf.reaper_master == "localhost" or "127.0.0.1":
            for reponame in conf.repositories:
                cmd_folder = "mkdir -p {0}".format(
                    self.localhost_repository_data_path
                )
                cmd = "reposync -p {0} -r {1}".format(
                    self.localhost_repository_data_path,
                    reponame
                )
                subprocess.check_output(cmd_folder, shell=True)
                subprocess.check_output(cmd, shell=True)
        else:
            for repo in conf.repositories:
                cmd = "reposync -p {0} -r {1}".format(
                    conf.repository_data_path,
                    repo
                )
                subprocess.check_output(cmd, shell=True)

    def create_metadata(self):
        """Create metadata for repository"""
        if conf.reaper_master == "localhost" or "127.0.0.1":
            repository_path = conf.localhost_repository_data_path
        else:
            repository_path = conf.repository_data_path

        for reponame in conf.repositories:
                cmd = "createrepo {0}/{1}".format(
                    repository_path,
                    reponame
                )
                subprocess.check_output(cmd, shell=True)

    def push_to_master(self):
        """Create folders on master and push new packages to the reaper master"""
        if conf.reaper_master == "localhost" or "127.0.0.1":
            print("push to master is not needed because the reaper_master is: localhost")
        else:
            cmd_folder = "ssh {0}@{1} 'mkdir -p {2}'".format(
                conf.remote_user,
                conf.reaper_master,
                conf.localhost_repository_data_path
            )
            cmd = "rsync -a {0} {1}:{2}".format(
                conf.repository_data_path,
                conf.reaper_master,
                conf.localhost_repository_data_path
            )
        subprocess.check_output(cmd_folder, shell=True)
        subprocess.check_output(cmd, shell=True)

if __name__ == "__main__":

    conf = Config()

    parser = argparse.ArgumentParser(description='reaper client functions')
    parser.add_argument(
        '-s',
        '--sync',
        action='store_true',
        help="get upstream repositories"
    )
    parser.add_argument(
        '-m',
        '--meta',
        action='store_true',
        help="create metadata for local stored repositories"
    )
    parser.add_argument(
        '-p',
        '--push',
        action='store_true',
        help="push repositories to master"
    )
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help="start all task's in this order: sync -> meta -> push"
    )
    args = vars(parser.parse_args())
    r = Repositories()
    if args['sync'] == True:
        r.get_upstream_packages()
    elif args['meta'] == True:
        r.create_metadata()
    elif args['push'] == True:
        r.push_to_master()
    elif args['all'] == True:
        r.get_upstream_packages()
        r.create_metadata()
        r.push_to_master()
    else:
        parser.print_help()
        sys.exit(1)
