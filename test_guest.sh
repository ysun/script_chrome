#!/bin/bash
#set -e
# USB update
# sudo scp 192.168.3.7:/home/chrome/chromeOS/tools/test_guest.sh .
# ./test_guest.sh copy
# ./test_guest.sh
# network update
# ./test_ssh.sh


# install expect
cd /home/ikvmgt/
echo Y | apt-get install expect

# set environment variables
sed -i '$a export PATH=$PATH:/usr/games' /etc/profile
source /etc/profile


# copy file
if [[ $1 == 'copy' ]];then
/usr/bin/expect<<EOF
set timeout 120
spawn scp -r 192.168.3.7:/home/chrome/chromeOS/tools/* .
expect {
	"(yes/no)" { send "yes\r"; exp_continue }
	"password:" { send "123456\r" }
}
expect eof
EOF
exit
fi


# ssh
/usr/bin/expect<<EOF
spawn "passwd"
expect "New password:"
send "123456\r"
expect "Retype new password:"
send "123456\r"
expect eof
EOF
/usr/sbin/sshd -f /home/ikvmgt/sshd_config
ps -ef |grep sshd


# stream
echo Y | apt-get install gcc
tar xvf stream.tar.gz
cd /home/ikvmgt/stream
gcc stream_omp.c -o stream
# ./stream


# netperf
cd /home/ikvmgt/
tar xvf netperf.tar.gz
cd /home/ikvmgt/netperf
apt-get install make
./configure
make
touch /usr/local/bin/test
make install
cd /home/ikvmgt/netperf/src/
netserver
if [ $?==0 ]
then
	# netperf -H localhost -t tcp_stream -l 60
	echo "successful"
else
	netserver -p 49999
fi


# fio
cd /home/ikvmgt/
echo Y | apt-get install fio
# fio -filename=test_file -direct=1 -iodepth 256 -rw=read -ioengine=libaio -size=2G -numjobs=4 -name=fio_read


# iperf3
echo Y | apt-get install iperf3
iperf3 -s -D
# iperf3 -c localhost -t 60 -P 10


# geekbenchLinux
tar xvf Geekbench-5.3.0-Linux.tar.gz
cd /home/ikvmgt/Geekbench-5.3.0-Linux
mkdir -p /data/local/tmp/
cp geekbench* /data/local/tmp/
/data/local/tmp/geekbench_x86_64 --unlock geekbench@intel.com LBLOH-LDXXG-EOTSO-CMU7C-4W225-R6YP5-M7TEI-7CCNR-UXYDE
# /data/local/tmp/geekbench_x86_64 --no-upload --cpu


# liunxKernel
cd /home/ikvmgt/
echo Y | apt-get install bc libssl-dev bison flex libelf-dev time
git clone https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
mkdir -p /build/eve/lib/firmware/i915/
cp kbl_guc_ver9_39.bin kbl_huc_ver02_00_1810.bin /build/eve/lib/firmware/i915
cp ATT51092.config ./linux
cd /home/ikvmgt/linux
mv ATT51092.config .config
make olddefconfig
# time make -j4


# nexuiz
cd /home/ikvmgt/
echo Y | apt-get install nexuiz
# nexuiz -benchmark demos/demo1


# openarena
echo Y | apt-get install openarena
mkdir -p /home/ikvmgt/.openarena/baseoa/demos/
cp /home/ikvmgt/anholt.cfg /home/ikvmgt/.openarena/baseoa/
cp /home/ikvmgt/anholt.dm_66 /home/ikvmgt/.openarena/baseoa/demos
# openarena +exec anholt


# gfxbench
echo Y | apt-get install apitrace
# glretrace gfxbench4/tessellation.trace
# glretrace gfxbench4/tar-chase.trace
# glretrace gfxbench4/manhattan.trace


# glmark2
echo Y | apt-get install git g++ build-essential pkg-config
echo Y | apt-get install libx11-dev libgl1-mesa-dev libjpeg-dev libpng-dev
echo Y | apt-get install python python3-pip
pip3 install paramiko
git clone https://github.com/glmark2/glmark2.git
cd /home/ikvmgt/glmark2/
./waf configure --with-flavors=x11-gl
./waf build -j 4
./waf install
strip -s /usr/local/bin/glmark2
# su --command=glmark2 ikvmgt

