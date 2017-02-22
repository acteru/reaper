# Reaper
Get your needed repositories on the slave nodes and push them to your master server where you have the possibility to create different deployment environments.

## Setup
![reaper](https://cloud.githubusercontent.com/assets/7287250/20973613/8f2722b6-bc99-11e6-9cd3-7b9ca90f5e9f.png)

## Requirements for CentOS/Rhel 7

Add epel-repo and install Python3

    yum install epel-release
    yum install python34 python34-pip
    pip3 install --upgrade pip
    pip3 install PyYAML

Make sure that ssh-keys are already exchanged between master and slave.

## Roadmap
* Master:
   * metadata creation for synced repositories
   * repo publishing
   * cli for master administration
