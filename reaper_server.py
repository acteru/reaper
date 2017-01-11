#!/usr/bin/env python

import yaml
import yum
import os
import sys
import subprocess
import errno
import platform
import argparse

class reaper:

    def __init__(self,clients,master_repo,os_version,arch,con_user,path,packagemanager):
        self.clients = clients
        self.master_repo = master_repo
        self.os_version = os_version
        self.arch = arch
        self.con_user = con_user
        self.path = path
        self.packagemanager = packagemanager


    def parse_commands(self):
        parser = argparse.ArgumentParser(prog=sys.argv[0])
        parser.add_argument('-s','--status',help="show current repository state")
        parser.add_argument('-x','--sync',help="syncs all clients to master")
        parser.add_argument('-b','--background',help="runs reaper in background")
        parser.add_argument('-i','--add-instance',help="add's new mastere instance")
        args = parser.parse_args()

    # install needed packages for reaper
    def check_installed_packages(self):
        yb = yum.YumBase()
        prereqs = ["httpd","createrepo","rsync"]
        for package in prereqs:
            print "Checking for required package: %s" % (package)
            res = yb.rpmdb.searchNevra(name=package)
            if res:
                for pkg in res:
                    print pkg, "installed"
            else:
                try:
                    print "trying to install missing package: %s" % (package)
                    yb.install(name=package)
                except:
                    print >> sys.stderr, "Failed during install of %s package!" % (package)
                    sys.exit(1)

    # show the current status of synced repositories
    def print_status(self):
        print "Print current synced repositories"


    # sync repository or repositories
    def sync_client(self,con_user,client,client_path,master_repo,arch,os_version):
        rsync_cmd = "rsync -az %s@%s:%s %s/%s/%s" % (con_user,client,client_path,master_repo,os_version,arch)
        try:
            subprocess.check_output(rsync_cmd, shell=True)
        except:
            print ("rsync not found --try yum install rsync")


    # sync all clients --default behavior
    def sync_all_clients(self,loaded_config,os_version):
        for client in loaded_config['sources']:
            path = loaded_config['sources'][client]['path']
            master_repo = loaded_config['master_repo']
            con_user = loaded_config['sources'][client]['user']
            arch = 'x86_64'
            reaper.sync_client(con_user,client,path,master_repo,arch,os_version)


    def create_metadata(self,loaded_config):
        master_repo = loaded_config['master_repo']
        repo_path = os.listdir(master_repo)
        try:
            for i in repo_path:
                cmd_createrepo = "createrepo %s/%s" % (master_repo,i)
                subprocess.check_output(cmd_createrepo, shell=True)
        except:
            print ("metadata creation failed")


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


class config_load:
    # load config
    def load_config(self):
        with open('config/master_config.yaml', 'r') as config_load:
            try:
                loaded_config = yaml.load(config_load)
                return loaded_config
            except yaml.YAMLError as exc:
                print exc


    # discover major/minor version of the clients
    def client_meta(self, client_addresses, con_user):
        for client in client_addresses:
            try:
                cmd_redhat_release = "scp %s@%s:/etc/redhat-release /dev/stdout" % (con_user, client)
                redhat_release = subprocess.check_output(cmd_redhat_release, shell=True)
                os_version = redhat_release.split(" ", 1)
                os_version = os_version[3].lower()
                return os_version
            except:
                print "client version not found"
                sys.exit(0)

    # all_clients
    def all_client_cmd(self,loaded_config,os_version):
        for client in loaded_config['sources']:
            path = loaded_config['sources'][client]['path']
            master_repo = loaded_config['master_repo']
            con_user = loaded_config['sources'][client]['user']
            arch = 'x86_64'
            all_clients = con_user, client, path, master_repo, arch, os_version
        return all_clients

    # check os
    def check_platform(self):
        os = platform.linux_distribution()
        if "Fedora" in os[0]:
            packagemanager = "dnf"
        elif os[0] in "CentOS" or "CentOS Linux" or "RedHat" or "Red Hat Enterprise Linux Server":
            packagemanager = "yum"
        else:
            print ("Your Operatingsystem is not supported please use CentOS, RHEL or Fedora")
            sys.exit()
        return(packagemanager)


if __name__ == "__main__":
    try:
        config = config_load()

        reaper = reaper()
        config = reaper.load_config()
        os_version = reaper.client_meta()
        reaper.check_installed_packages()
        reaper.sync_all_clients(config,os_version)
        reaper.create_metadata(config)

    except KeyboardInterrupt:
        sys.exit(0)
