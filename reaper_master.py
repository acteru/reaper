#!/usr/bin/python3

"""
Manage repository releases - on master reposerver
new releases are created with lv-snapshots

"""

import datetime
import subprocess
import yaml
import os
import sys

class RepositorieRelease():
    """Create new releases for Repositories"""
    def __init__(self, release_name, vg_origin, lv_origin, lv_name, lv_size, repo_path):
        self.date_today = datetime.date.today()
        self.release_name = release_name
        self.repo_path = repo_path
        self.vg_origin = vg_origin
        self.lv_origin = lv_origin
        self.lv_name = lv_name
        self.lv_size = lv_size
        self.mount_path = "{0}/{1}".format(self.repo_path, self.release_name)
        self.snapshot_name = "release--{0}-{1}".format(self.date_today, self.lv_name)

    def create_repo_snapshot(self):
        """Create snapshot of a logical volume"""
        create_snapshot = "lvcreate -pr --snapshot -L {0} --name {1} {2}".format(self.lv_size, self.snapshot_name, self.lv_origin)
        print(create_snapshot)
        #subprocess.check_output(create_snapshot, shell=True)
        return print("snapshot: {0} of {1} has successfully been created".format(self.snapshot_name, self.lv_origin))

    def create_mountpoint(self):
        """Create mountpoint for the new snapshot"""
        mount_cmd = "mkdir -p {0}".format(self.mount_path)
        print(mount_cmd)
        #subprocess.check_output(mount_cmd, shell=True)
        return print("mountpoint {0} has successfuly been created".format(self.mount_path))
        
    def mount_snapshot(self):
        """Mount new made snapshot on mountpoint"""
        mount_path = "/srv/{0}".format(self.release_name)
        mount_cmd = "mount /dev/{0}/release-{1}-{2} {3}".format(self.vg_origin, self.date_today, self.lv_name, mount_path)
        print(mount_cmd)
        #subprocess.check_output(mount_cmd, shell=True)
        
    def create_symlink(self):
        """Create symlink to webserver docroot"""
        symlink_cmd = "ln -s {0}".format(self.mount_path)
        print(symlink_cmd)
        #subprocess.check_output(symlink_cmd, shell=True)

    def get_snapshot_list(self):
        """List all lv snapshots on the system"""
        get_snapshot_cmd = "lvs -o lv_name,lv_attr --noheadings -S lv_attr=~[^s.*]"
        subprocess.check_output(get_snapshot_cmd, shell=True)


if __name__ == "__main__":

    if not os.getuid() == 0:
        """Check if root user is used"""
        sys.exit('Script must be run as root')
    
    #TODO create argsparser / configuration file for data" 
    r = RepositorieRelease("stable", "repo-data", "/dev/repo-data/repo01", "stabel", "10G", "/srv")
    r.create_repo_snapshot()
    r.create_mountpoint()
    r.mount_snapshot()
    r.create_symlink()
    r.get_snapshot_list()
