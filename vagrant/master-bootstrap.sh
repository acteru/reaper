#!/usr/bin/env bash
yum install httpd nginx wget epel-release createrepo git -y
# clone reaper
git clone https://github.com/acteru/reaper.git /opt/reaper
# create folders
mkdir -p /srv/reaper/latest
mkdir -p /srv/reaper/releases
# start webserver
systemctl start httpd
