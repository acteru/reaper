#!/usr/bin/env bash
yum update -y
yum install git epel-release -y
git clone https://github.com/acteru/reaper.git
yum update -y
yum install python-pip -y
sudo pip install --upgrade pip
sudo pip install PyYAML
mkfs.ext4 /dev/vdb
mkdir -p /var/repo
mount /dev/vdb /var/repo
