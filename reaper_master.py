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
    def __init__(self, release_name, vg_origin, lv_origin, lv_name, lv_size, repo_path, document_root):
        self.date_today = datetime.date.today()
        self.release_name = release_name                                      # stable or new_release for path: /srv/stable
        self.repo_path = repo_path                                            # default: /srv location to repositories 
        self.document_root = document_root                                    # apache document_root
        self.vg_origin = vg_origin                                            # main vg for repositories
        self.lv_origin = lv_origin                                            # origin lv on main vg
        self.lv_name = lv_name                                                # name for snapshot
        self.lv_size = lv_size                                                # size for snapshot
        self.mount_path = "{0}/{1}".format(self.repo_path, self.release_name) # bsp. '/srv/stable'
        self.snapshot_name = "release-{0}-{1}".format(self.date_today, self.lv_name) # "release-date-snapshot_name

    def create_repo_snapshot(self):
        """Create snapshot of a logical volume"""
        create_snapshot = "lvcreate -pr --snapshot -L {0} --name {1} {2}".format(self.lv_size, self.snapshot_name, self.lv_origin)
        print(create_snapshot)
        #subprocess.check_output(create_snapshot, shell=True)
        return print("snapshot: {0} of {1} has successfully been created".format(self.snapshot_name, self.lv_origin))


    def create_mountpoint(self):
        """Create mountpoint for the new snapshot"""
        if not os.path.exists(self.mount_path):
            os.makedirs(self.mount_path)
            return print("mountpoint {0} has successfuly been created".format(self.mount_path))

        
    def mount_snapshot(self):
        """Mount new made snapshot on mountpoint"""
        mount_path = "{0}/{1}".format(self.repo_path, self.release_name)
        mount_cmd = "mount /dev/{0}/release-{1}-{2} {3}".format(self.vg_origin, self.date_today, self.lv_name, mount_path)
        subprocess.check_output(mount_cmd, shell=True)

        
    def check_symlink(self):
        """Create symlink to webserver docroot"""
        src = self.mount_path
        dst = self.document_root + "/" + self.release_name
        if os.path.islink(dst) == True:
            print("symlink for release alrady exists")
        else:
            os.symlink(src, dst)
            print("new symlink to {0} created".format(dst))


    def check_mount(self):
        """Check if other snapshot is already mounted"""
        check_if_mounted = "grep -qs '{0}' /proc/mounts".format(self.mount_path)
        if subprocess.call(check_if_mounted) == 0:
            subprocess.check_output("umount {0}".format(self.mount_path))
            mount_snapshot()
        else:
            mount_snapshot()


    def get_snapshot_list(self):
        """List all lv snapshots on the system"""
        get_snapshot_cmd = "lvs -o lv_name,lv_attr --noheadings -S lv_attr=~[^s.*]"
        subprocess.check_output(get_snapshot_cmd, shell=True)


if __name__ == "__main__":

    if not os.getuid() == 0:
        """Check if root user is used"""
        sys.exit('Script must be run as root')
    
    #TODO create argsparser / configuration file for data" 
    r = RepositorieRelease("stable", "repo-data", "/dev/repo-data/repo01", "stabel", "10G", "/srv", "/var/www/html")
    r.create_repo_snapshot()
    r.create_mountpoint()
    #r.mount_snapshot()
    r.check_symlink()
    r.get_snapshot_list()
    #r.check_and_mount()
