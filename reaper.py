import platform
import subprocess
import sys
import yum

def check_platform(repo_path):
    repo_path = repo_path
    os = platform.linux_distribution()
    if "Fedora" in os[0]:
        set_packagemanager = "dnf"
        set_repo_path = ( "%s/fedora/%s/" % repo_path, os[1] ) 
    elif "Centos" in os:
        set_packagemanager = "yum"
        if "7" in os[0]:
            set_repo_path = ( "'%s'/centos/'%s'/" % repo_path, os[1] )
        else:
            set_repo_path = ( "'%s'/centos/'%s'/" % repo_path, os[1] )
    else:
        sys.exit()
    return(set_packagemanager,set_repo_path)

def sync_repos(packagemanager):
    if packagemanager == 'dnf':
        sync_repos_cmd = ( "dnf reposync -p '%s'" % repo_path )
        sync = subprocess.check_output(sync_repos_cmd, shell=True)
    else:
        sync_repos_cmd = ("reposync -p '%s'" % repo_path) 
        subprocess.check_output(sync_repos_cmd, shell=True)

def main():
    repo_path = '/var/repo/'
    packagemanager = (check_platform(repo_path))
    print packagemanager[0]
    print packagemanager[1]
    #sync_repos(packagemanager)

main()
