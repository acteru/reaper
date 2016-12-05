import platform
import subprocess
import sys
import yum

def get_platform():
    os = platform.linux_distribution()
    if "Fedora" in os:
        set_packagemanager = "dnf"
    elif "Centos" in os:
        set_packagemanager = "yum"
    else:
        sys.exit()
    return(set_packagemanager)

def get_repoid(packagemanager):
    manager_cmd = ("%s repolist | awk '/repo id/{y=1;next}y' | awk '{print $1'}" % packagemanager)
    repolist = subprocess.check_output(manager_cmd , shell=True)
    repolist = repolist.split('\n')
#    if 'repolist:' in repolist: repolist.remove('repolist:')
    print repolist
#    if "/" in repolist: 
#        for i in repolist:
#            m = i.index('/')
#            l = i[:m]
#            print l
#    else:
#        print repolist

def main():
    packagemanager = (get_platform())
    get_repoid(packagemanager)

main()
