#!/usr/bin/env bash
yum install httpd nginx wget epel-release createrepo -y
# start webserver
systemctl start httpd
