#!/usr/bin/env python

import platform
import subprocess
import sys
import os
import errno
import yaml


sys.tracebacklimit = 0

class Config():
    def load_config(self):
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
            repo_path = ("%s/fedora/%s/x86_64" % (repo_path,os[1]))
        elif "CentOS" in os[0]:
            packagemanager = "yum"
            repo_path = ("%s/centos/%s/x86_64" % (repo_path,os[1]))
        elif "CentOS Linux" in os[0]:
            packagemanager = "yum"
            repo_path = ("%s/centos/%s/x86_64" % (repo_path,os[1]))
        elif "RedHat" in os[0]:
            packagemanager = "yum"
            repo_path = ("%s/redhat/%s/x86_64" % (repo_path,os[1]))
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
            subprocess.check_output(sync_repos_cmd, shell=True)
        else:
            sync_repos_cmd = ("reposync -p %s" % (repo_path))
            subprocess.check_output(sync_repos_cmd, shell=True)


if __name__ == "__main__":
    config = Config()
    repo_path = config.load_config()['repo_path']
    reposync = RepoSync(repo_path)
    pathpackage = reposync.check_platform(repo_path)
    reposync.create_repo_dir(pathpackage[1])
    reposync.sync_repos(pathpackage[0],pathpackage[1])