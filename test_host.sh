#!/bin/bash
#set -e
# scp 192.168.3.7:/home/chrome/chromeOS/tools/test_host.sh .
# bash ./test_host.sh reboot
# ./test_host.sh copy
# "curl -Ls https://raw.github.com/skycocker/chromebrew/master/install.sh | bash" at chronos
# ./test_host.sh


# Read-write partition
if [[ $1 == 'reboot' ]]
then
	cd /usr/share/vboot/bin/
	crossystem dev_boot_signed_only=0
	crossystem dev_boot_usb=1
	crossystem dev_default_boot=usb
	./make_dev_ssd.sh --remove_rootfs_verification --partitions 4
	./make_dev_ssd.sh --remove_rootfs_verification --partitions 2
	mount -o remount,rw,exec /mnt/stateful_partition/
	reboot
	exit
fi


# install crew
su chronos -c 'crew --version'
if [ $? != 0 ]
then
	echo "Please execute the following command manually at chronos"
	echo "curl -Ls https://raw.github.com/skycocker/chromebrew/master/install.sh | bash"
	exit
else
	echo "crew installed!"
fi


# install expect paramiko expect   
su chronos -c 'echo Y | crew install expect'
pip install paramiko

# copy file
if [[ $1 == 'copy' ]];then
/usr/local/bin/expect<<EOF
set timeout 100
spawn scp -r root@192.168.3.7:/home/chrome/chromeOS/tools/* ./ 
expect "password"
send "123456\r"
expect eof
EOF
exit
fi


# stream
cd /mnt/stateful_partition/
tar xvf stream.tar.gz
cd /mnt/stateful_partition/stream
gcc stream_omp.c -o stream
# mount -o remount,rw,exec /mnt/stateful_partition/
./stream


# fio
# fio -filename=test_file -direct=1 -iodepth 256 -rw=read -ioengine=libaio -size=2G -numjobs=4 -name=fio_read


# iperf3
iperf3 -s -D
#iperf3 -c localhost -t 60 -P 10


# netperf
cd /mnt/stateful_partition/
tar xvf netperf.tar.gz
cd /mnt/stateful_partition/netperf
./configure
sleep 10
make
touch /usr/local/bin/test
make install
cd ./src
netserver        
if [ $?==0 ]
then
	echo "successful"
	netperf -H localhost -t tcp_stream -l 60
else
	netserver -p 49999
fi


# geekbenchLinux
cd /mnt/stateful_partition/
tar xvf Geekbench-5.3.0-Linux.tar.gz
cd Geekbench-5.3.0-Linux
mkdir -p /mnt/stateful_partition/data/local/tmp/
cp geekbench* /mnt/stateful_partition/data/local/tmp/
su chronos --command='/mnt/stateful_partition/data/local/tmp/geekbench_x86_64 --unlock geekbench@intel.com LBLOH-LDXXG-EOTSO-CMU7C-4W225-R6YP5-M7TEI-7CCNR-UXYDE'
su chronos --command='/mnt/stateful_partition/data/local/tmp/geekbench_x86_64 --cpu --no-upload'


# geekbenchAndroid
cd /mnt/stateful_partition/
tar xvf Geekbench-5.3.0-Android-Corporate.tar.gz
cd Geekbench-5.3.0-Android-Corporate
adb devices
if [ $? -eq 0 ]
then
	adb push geekbench* /data/local/tmp/
	adb shell /data/local/tmp/geekbench_x_86_64 --unlock geekbench@intel.com LBLOH-LDXXG-EOTSO-CMU7C-4W225-R6YP5-M7TEI-7CCNR-UXYDE
	adb shell /data/local/tmp/geekbench_x86_64 --no-upload --cpu
else
	echo "adb devices not open debugging"
fi


# Android-fio
cd /mnt/stateful_partition/
adb push ./Storage_FIO/* /data/local/tmp/
adb shell /date/local/tmp/fio -direct=1 -ioengine=libaio -size=512M -name=/data/local/tmp/fio_read –group_reporting –runtime=600 –bs=4k -rw=write 


# blogbench


# linux_kernel
#mount -o remount,rw,exec /mnt/stateful_partition/
mkdir -p /build/eve/lib/firmware/i915/
cd /mnt/stateful_partition/
cp ./kbl_guc_ver9_39.bin /build/eve/lib/firmware/i915/
cp ./kbl_huc_ver02_00_1810.bin /build/eve/lib/firmware/i915/
git clone https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git
cp inat-tables.c ATT51092.config ./linux/
cd /usr/local/lib64/
ln -s libreadline.so.8.0 libreadline.so.6
cd /mnt/stateful_partition/linux
mv ATT51092.config .config 
su --command='crew install bc' chronos
cp /usr/local/lib64/libreadline.so.8.0 /mnt/stateful_partition/
cp /mnt/stateful_partition/libreadline.so.6 /usr/local/lib64/
make olddefconfig
# time make -j4


# chroot
cd /mnt/stateful_partition/
git clone https://github.com/dnschneid/crouton.git
/usr/local/bin/expect<<EOF
set timeout -1 
spawn ./crouton/installer/crouton -r buster -t xfce
expect "Please"
send "intel\r"
expect "New password:"
send "123456\r"
expect "password:"
send "123456\r"
expect eof
EOF
enter-chroot

