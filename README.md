# Reaper
Get your needed repositories on the slave nodes and push them to your master server where you have the possibility to create different deployment environments.

## Requirements for CentOS/RHEL7 & CentOS/RHEL6

    yum install epel-release -y

    yum install python34 python34-PyYAML createrepo rsync git -y


## Usage

    git clone https://github.com/acteru/reaper.git /opt/reaper

    vim /opt/reaper/config.yaml (edit - add your needs)

    ./reaper.py --help
    usage: reaper.py [-h] [-s] [-m] [-p] [-a]

    trigger reaper functions

    optional arguments:
    -h, --help  show this help message and exit
    -s, --sync  get upstream repositories
    -m, --meta  create metadata for repositories
    -p, --push  push repositories to master
    -a, --all   start all task's in this order sync->meta->push

## Server configuration
Ansible playbooks coming soon


## Management on Master

Make sure that ssh-keys are already exchanged between master and slave.
