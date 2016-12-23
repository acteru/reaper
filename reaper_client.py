#!/usr/bin/env python

import platform
import subprocess
import sys
import os
import errno
import yaml


sys.tracebacklimit = 0


def load_config():
    with open('config/client_config.yaml', 'r') as config_load:
        try:
            loaded_config = yaml.load(config_load)
            return loaded_config
        except yaml.YAMLError as exc:
            print exc

class RepoSync():


    def __init__(self,repo_path):
        self.repo_path = repo_path


    def check_platform(self,repo_path):
        repo_path = repo_path
        os = platform.linux_distribution()
        if "Fedora" in os[0]:
            packagemanager = "dnf"
            repo_path = ("%s/fedora/%s" % (repo_path, os[1]))
        elif "CentOS" in os[0]:
            packagemanager = "yum"
            repo_path = ("%s/centos/%s" % (repo_path, os[1]))
        elif "CentOS Linux" in os[0]:
            packagemanager = "yum"
            repo_path = ("%s/centos/%s" % (repo_path, os[1]))
        elif "RedHat" in os[0]:
            packagemanager = "yum"
            repo_path = ("%s/redhat/%s" % (repo_path, os[1]))
        else:
            print ("Your Operatingsystem is not supported please use CentOS, RHEL or Fedora")
            sys.exit()
        return(packagemanager,repo_path)


    def create_repo_dir(self,path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
               raise


    def sync_repos(self,packagemanager,repo_path):
        if packagemanager == 'dnf':
            sync_repos_cmd = ("dnf reposync -p %s" % (repo_path))
            print sync_repos_cmd
            subprocess.check_output(sync_repos_cmd, shell=True)
        else:
            sync_repos_cmd = ("reposync -p %s" % (repo_path))
            print sync_repos_cmd


if __name__ == "__main__":
    repo_path = load_config()['repo_path']
    reposync = RepoSync(repo_path)
    pathpackage = reposync.check_platform(repo_path)
    reposync.create_repo_dir(pathpackage[1])
    reposync.sync_repos(pathpackage[0],pathpackage[1])