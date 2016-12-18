## Vagrant-Setup
it is assumed that libvirt is used as the provider. Set an env variable for vagrant to set the default provider:
`export VAGRANT_DEFAULT_PROVIDER=libvirt`
### vagrant install
#### Ubuntu
`wget https://releases.hashicorp.com/vagrant/1.9.1/vagrant_1.9.1_x86_64.deb; dpkg -i vagrant_1.9.1_x86_64.deb`
#### Centos/Fedora
`yum install wget -y; wget https://releases.hashicorp.com/vagrant/1.9.1/vagrant_1.9.1_x86_64.rpm; yum localinstall vagrant_1.9.1_x86_64.rpm -y`
#### Fedora 25
`dnf install wget -y; wget https://releases.hashicorp.com/vagrant/1.9.1/vagrant_1.9.1_x86_64.rpm; dnf install vagrant_1.9.1_x86_64.rpm -y`
### libvirt provider
#### Ubuntu
`sudo apt install qemu libvirt-bin ebtables dnsmasq libxslt-dev libxml2-dev libvirt-dev zlib1g-dev ruby-dev ruby-libvirt`
#### Centos 6,7,Fedora 21
`sudo yum install qemu libvirt libvirt-devel ruby-devel gcc qemu-kvm -y`
#### Fedora 22 and up
`sudo dnf -y install qemu libvirt libvirt-devel ruby-devel gcc`
## Install vagrant and libvirt Plugin:
`sudo dnf install vagrant vagrant-libvirt`
#### Arch
`pacman -Sy vagrant`

After vagrant and the dependecies are install now install the libvirt plugin:
vagrant plugin install vagrant-libvirt
now your all set!
### Usefull vagrant commands
* vagrant up        = "start vm"
* vagrant halt      = "stop vm"
* vagrant destory   = "destorys the vm"
* vagrant ssh       = "connects as the vagrant user to the box as the vagrant user (sudo)"
