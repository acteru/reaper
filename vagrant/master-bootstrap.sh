#!/usr/bin/env bash
yum install httpd nginx wget epel-release createrepo -y
# create folders
mkdir -p /srv/latest
mkdir -p /srv/stable
# start webserver
systemctl start httpd
