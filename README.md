# Reaper
Get your needed repositories on the slave nodes and push them to your master server where you have the possibility to create different deployment environments.

## Requirements for CentOS/RHEL7

    yum install epel-release

    yum install python34 python34-pip createrepo rsync  

    pip3 install --upgrade pip

    pip3 install PyYAML

Make sure that ssh-keys are already exchanged between master and slave.
