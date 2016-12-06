import platform
import subprocess
import sys
import os
import errno
import yum

# creates repofolders and sync all enabled repositories

def check_platform(repo_path):
    repo_path = repo_path
    os = platform.linux_distribution()
    if "Fedora" in os[0]:
        set_packagemanager = "dnf"
        set_repo_path = ("%s/fedora/%s" % (repo_path, os[1])) 
    elif "Centos" in os[0]:
        set_packagemanager = "yum"
        set_repo_path = ("%s/centos/%s" % (repo_path, os[1]))
    elif "RedHat" in os[0]:
        set_packagemanager = "yum"
        set_repo_path = ("%s/redhat/%s" % (repo_path, os[1]))
    else:
        sys.exit()
    return(set_packagemanager,set_repo_path)

def ensure_repo_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def sync_repos(packagemanager,set_repo_path):
    if packagemanager == 'dnf':
        sync_repos_cmd = ("dnf reposync -p %s" % (set_repo_path))
        print sync_repos_cmd
        #sync = subprocess.check_output(sync_repos_cmd, shell=True)
    else:
        sync_repos_cmd = ("reposync -p %s" % (set_repo_path)) 
        print sync_repos_cmd
        #subprocess.check_output(sync_repos_cmd, shell=True)

def main():
    repo_path = '/var/repo'
    pathpackage = (check_platform(repo_path))
    print pathpackage[1]
    ensure_repo_dir(pathpackage[1])
    #sync_repos(pathpackage[0],pathpackage[1])
main()
