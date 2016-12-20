#!/usr/bin/env bash
PKG=${1:-yum}
$PKG update -y
$PKG install git ${2:-PyYAML} -y
mkdir -p /var/repo

if cd /opt/reaper; then
    git pull
else
    git clone https://github.com/acteru/reaper.git /opt/reaper
fi
