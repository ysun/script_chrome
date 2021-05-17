#!/bin/bash
# set -e

# sudo apt-get install net-tools
# sudo apt-get install openssh-client
# export PATH=/usr/games/:$PATH
# sudo scp 192.168.3.7:/home/chrome/chromeOS/tools/test_chroot.sh .
# ./test_chroot.sh copy
# ./test_chroot.sh


cd /home/intel/
apt-get update -y
echo Y | apt-get install expect git python3-pip curl
pip3 install paramiko

# set environment variables
sed -i '$a export PATH=$PATH:/usr/games' /etc/profile
source /etc/profile

# copy file
if [[ $1 == 'copy' ]];then
/usr/bin/expect<<EOF
set timeout 120
spawn scp -r root@192.168.3.7:/home/chrome/chromeOS/tools/* /home/intel/
expect {
	"yes/no" { send "yes\r";exp_continue }
	"password:" { send "123456\r" }
}
expect eof
EOF
exit
fi


# nexuiz
cd /home/intel/
echo Y | apt-get install nexuiz
nexuiz -benchmark demos/demo1


# openarena
echo Y | apt-get install openarena
mkdir -p /home/intel/.openarena/baseoa/demos
cp /home/intel/anholt.cfg /home/intel/.openarena/baseoa/
cp /home/intel/anholt.dm_66 /home/intel/.openarena/baseoa/demos
su intel -c 'openarena +exec anholt'


# gfxbench4
echo Y | apt-get install apitrace
# glretrace gfxbench4/t-rex.trace


# glmark
echo Y | apt-get install git g++ build-essential pkg-config libx11-dev libgl1-mesa-dev libjpeg-dev libpng-dev python
git clone https://github.com/glmark2/glmark2.git
cd /home/intel/glmark2
./waf configure --with-flavors=x11-gl
./waf build -j 4
./waf install
strip -s /usr/local/bin/glmark2
cd /home/intel/
su --command=glmark2 intel
