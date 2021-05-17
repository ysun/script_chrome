#!/bin/bash

set -e

copySSH(){
/usr/bin/expect<<EOF
set timeout 120
spawn scp 192.168.3.102:/etc/ssh/sshd_config /home/ikvmgt/
expect "*word:"
send "test0000\r"
expect eof
EOF
sed -i -e '6,7d' -e '10s/no/yes/g' /home/ikvmgt/sshd_config
}

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
