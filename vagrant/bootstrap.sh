#!/usr/bin/env bash
mkdir -p /var/repo

if cd /opt/reaper; then
    git pull
else
    git clone https://github.com/acteru/reaper.git /opt/reaper
fi
