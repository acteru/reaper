#!/usr/bin/python3
import logging
import subprocess
import sys
import argparse
import os
import yaml
import platform

def config_load():
    """ return configuration from yaml """
    with open('./config.yaml', 'r') as config_load:
        try:
            return yaml.load(config_load)
        except:
            print(yaml.YAMLError)

def get_platform_information():
    """check the current platform"""
    os_platform = platform.dist()
    if os_platform[0] != '':
        return os_platform
    else:
        print("os name/version not found!")
        sys.exit(1)

def get_upstream_packages():
    """create folder for repo and sync packages"""

def create_metadata():
    """create meta data for repositories"""

def push_to_master():
    """Create folders on master and push new packages to the reaper master"""

def cli():
    parser = argparse.ArgumentParser(description='reaper client functions')
    parser.add_argument(
        '-s',
        '--sync',
        action='store_true',
        help="get upstream repositories"
    )
    parser.add_argument(
        '-c',
        '--config',
        action='store_true',
        help="show configuration"
    )
    parser.add_argument(
        '-o',
        '--platform',
        action='store_true',
        help="show local platform"
    )
    parser.add_argument(
        '-m',
        '--meta',
        action='store_true',
        help="create metadata for local stored repositories"
    )
    parser.add_argument(
        '-p',
        '--push',
        action='store_true',
        help="push repositories to master"
    )
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help="start all task's in this order: sync -> meta -> push"
    )
    return vars(parser.parse_args())


if __name__ == "__main__":
    conf = config_load()
    platform = get_platform_information()
    args = cli()

    if args['config'] == True:
        print(conf.items())
    elif args['platform'] == True:
        get_platform_information()
    elif args['meta'] == True:
        create_metadata()
    elif args['push'] == True:
        push_to_master()
    elif args['all'] == True:
        get_upstream_packages()
        create_metadata()
        push_to_master()
    else:
        parser.print_help()
        sys.exit(1)
