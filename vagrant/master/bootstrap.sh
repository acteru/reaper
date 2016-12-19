#!/usr/bin/env bash
# install updates and add webservers
yum update -y
yum install httpd nginx git wget epel-release -y
yum install python-pip -y
# install Yaml for python
pip install --upgrade pip
pip install PyYAML
# Add space for the repositories
mkfs.ext4 /dev/vdb
mkdir -p /var/repo
mount /dev/vdb /var/repo
# start webserver
sudo systemctl start httpd
# get reaper
git clone https://github.com/acteru/reaper.git
