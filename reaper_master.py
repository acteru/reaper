#!/usr/bin/python3

"""
Manage repository releases - on master reposerver

reaper makes use of logicalvolumes to create snapshots of repositories and create
so called "releases". After creating a new release you can link it to your 
webserver where your repositories can be distributed.

"""

import datetime
import logging
import subprocess
import argparse
import yaml
import os
import sys


class Config():
    """Loads yaml configuration file and deserialize the reaper_master config"""
    def __init__(self):
        with open('./master_config.yaml', 'r') as config_load:
            try:
                config = yaml.load(config_load)
                # logging_config
                self.logfile_path = config["logfile_path"]
                self.loglevel_console = config["loglevel_console"]
                self.loglevel_file = config["loglevel_file"]
                # master_config
                self.document_root = config["document_root"]
                self.volumegroup = config["volumegroup"]
                self.logicalvolume = config["logicalvolume"]
            except:
                print(yaml.YAMLError)


class RepositoryRelease():
    """create new lv_snapshot releases form latest folder"""
    def __init__(
        self,
        volumegroup,
        logicalvolume,
        ):
        self.date_today = datetime.date.today()
        self.volumegroup = volumegroup
        self.logicalvolume = logicalvolume
        self.data_path = "/srv/reaper"
        self.snapshot_home = "/releases/"
        self.snapshot_size = "10G"
        self.snapshot_path = "{0}/{1}".format(self.data_path, self.snapshot_home)
        self.snapshot_name = "release-{0}".format(self.date_today)
        self.snapshot_full_path = self.snapshot_path + self.snapshot_name
        self.snapshot_lv_path = "/dev/{0}/{1}".format(
            volumegroup,
            self.snapshot_name
        )

    def check_snapshot(self):
        """check if snapshot already exists"""
        if os.path.islink(self.snapshot_lv_path) == True:
            print("snapshot {0} already exists".format(self.snapshot_lv_path))
            sys.exit(1)
        else:
            pass

    def create_repo_snapshot(self):
        """create snapshot of a logical volume"""
        create_snapshot = "lvcreate -pr --snapshot -L {0} --name {1} {2}/{3}".format(
        self.snapshot_size,
        self.snapshot_name,
        self.volumegroup,
        self.logicalvolume)
        print(create_snapshot)
        subprocess.check_output(create_snapshot, shell=True)
        print("snapshot: {0} of {1} has successfully been created".format(
            self.snapshot_name,
            self.logicalvolume)
        )

    def create_repo_mountpoint(self):
        """create folder for snapshot"""
        if not os.path.exists(self.snapshot_full_path):
            os.makedirs(self.snapshot_full_path)
            print("mountpoint for {0} has successfully been created".format(self.snapshot_full_path))

    def mount_repo_snapshot(self):
        """mount new made snapshot on mountpoint"""
        mount_cmd = "mount -o ro /dev/{0}/release-{1} {2}".format(
        self.volumegroup,
        self.date_today,
        self.snapshot_full_path)
        subprocess.check_output(mount_cmd, shell=True)
        print("{0} is mounted".format(self.snapshot_full_path))

    def create_fstab_entry(self):
        """create fstab entry for release"""
        pass

    def remove_release(self, snapshot_name):
        """remove snapshot and mountpoint"""
        snapshot_mount_path = "/srv/reaper/releases/{0}".format(snapshot_name)
        unmount_cmd = "umount {0}".format(snapshot_mount_path)
        lvremove_cmd = "lvremove /dev/{0}/{1} -y".format(self.volumegroup, snapshot_name)
        subprocess.check_output(unmount_cmd, shell=True)
        subprocess.check_output(lvremove_cmd, shell=True)
        os.rmdir(snapshot_mount_path)

    def set_snapshot(self, snapshot_name, instance_name):
        """set specifical release to instance"""
        src = "/srv/reaper/releases/{0}".format(snapshot_name)
        dst = conf.document_root + "/" + instance_name
        os.symlink(src, dst)
 
class cli():
    """extended cli function call"""
    def get_snapshot_list(self):
        """list all lv snapshots on the system as strings in list"""
        get_snapshot_cmd = "lvs -o lv_name,lv_attr --noheadings -S lv_attr=~[^s.*]"
        snapshots = subprocess.check_output(get_snapshot_cmd, shell=True)
        snapshots = str(snapshots, 'utf-8')
        snapshots = snapshots.split()
        print(snapshots)

if __name__ == "__main__":
    if not os.getuid() == 0:
        """check if root user is used"""
        sys.exit('Script must be run as root')

    ## create needed folders ##
    folder_list = ["/srv/reaper", "/srv/reaper/latest", "/srv/reaper/releases"]
    for folder in folder_list:
        if not os.path.exists(folder):
            os.makedirs(folder)

    ## load configuration ##
    conf = Config()
    logfile_path = conf.logfile_path + "/reaper.log"
    if not os.path.exists(logfile_path):
        touch_cmd = "touch " + logfile_path
        os.makedirs(conf.logfile_path)
        subprocess.check_output(touch_cmd, shell=True)

    ## configure logging ##
    logging.basicConfig(
        filename=logfile_path,
        level=conf.loglevel_file.upper(),
        format='%(asctime)s %(message)s'
    )

    ## create args parser ##
    parser = argparse.ArgumentParser(
        description='Manages repository releases',
        epilog="Example of use:" \
            "--setsnapshot release-2017-03-27 development" \
    )
    parser.add_argument(
        '-s',
        '--snapshots',
         action='store_true',
         help="list all repository snapshots on the system"
    )
    parser.add_argument(
        '-x',
        '--setsnapshot',
        action='store_true',
        help="set softlink from document root to a release"
    )
    parser.add_argument(
        '-r',
        '--release',
        action='store_true',
        help="create new release: creates snapshot and mount in /srv/reaper/releases/release-<date>"
    )
    parser.add_argument(
        "snapshotname",
        nargs='?',
        type=str,
        help="snapshot name"
    )
    parser.add_argument(
        "instancename",
        nargs='?',
        type=str,
        help="instance name"
    )
    parser.add_argument(
        '-d',
        '--deleterelease',
         action='store_true',
        help="remove specific release: unmount,remove snapshot, remove mountpoint"
    )
 
    args = vars(parser.parse_args())
    r = RepositoryRelease(
        conf.volumegroup,
        conf.logicalvolume,
    )

    ## validate user input to args parser ##
    if args['snapshots'] == True:
        cli = cli()
        cli.get_snapshot_list()
    elif args['setsnapshot'] == True and args['snapshotname'] and args['instancename']:
        r.set_snapshot(args['snapshotname'],args['instancename'])
    elif args['release'] == True:
        r.check_snapshot()
        r.create_repo_snapshot()
        r.create_repo_mountpoint()
        r.mount_repo_snapshot()
    elif args['deleterelease'] == True and args['snapshotname']:
        r.remove_release(args['snapshotname'])
    else:
        parser.print_help()
        sys.exit(1)
