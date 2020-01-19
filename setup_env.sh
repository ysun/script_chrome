#!/bin/bash
#set -x
set -e

mount -o remount,exec /mnt/stateful_partition/
echo "Remount /mnt/stateful_partition as executable"

iptables -F
iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT
echo "Deleted rules and forced all default policies accepted"
