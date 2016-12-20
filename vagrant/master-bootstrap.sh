#!/usr/bin/env bash
yum install httpd nginx wget epel-release -y
# start webserver
systemctl start httpd
