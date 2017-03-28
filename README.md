# Reaper
Get your needed repositories on the slave nodes and push them to your master server where you have the possibility to create auto lvsnapshots of your repositories. This snapshots are called releases and the can be linked to variouse instances like: test, integration, production.  Distribute them with a webserver of your choise and add your repositories to your target servers. In the examples the apache server is used but feel free to use something else just add the document\_root path to the configuration file.

## Requirements for CentOS/RHEL7

    yum install epel-release

    yum install python34 python34-pip createrepo rsync

    pip3 install --upgrade pip

    pip3 install PyYAML

## How to install reaper client
For example: setup a CentOS 7 Server and make sure that your needed repositories are attached to your server, this is also working for RedHat Enterprice Linux assuming you have the required subscriptions.

    sudo git clone https://github.com/acteru/reaper.git /opt/reaper

    mkdir -p /srv/reaper/repo

    vi /opt/reaper/config.yaml

    ssh-keygen

    ssh-copy-id root@reaper-master.example.com

## How to install reaper master
This is just an example to explain how it could work, you have the option to configure your own volumegroup and logicalvolume in the configuration file.

    git clone https://github.com/acteru/reaper.git /opt/reaper

    pvcreate /dev/vdb

    vgcreate repo-data /dev/vdb

    lvcreate -n repo01 -L 500G repo-data

    mkfs.ext4 /dev/repo-data/repo01

    vi /opt/reaper/master_config.yaml

    configure your own: volumegroup and logicalvolume


## Server configuration
Ansible playbooks coming soon


## Management on Master
Make sure that ssh-keys are already exchanged between master and slave. It is important to use lvm because reaper uses lvm snapshots to provide new releases of your repositories.
