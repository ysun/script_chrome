#!/bin/bash
#set -x
set -e

for((i=0; i<4; i++)) {
	cat /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_max_freq > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_min_freq
	echo "Force cpu${i} max frequency, now is `cat /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_cur_freq`"
	sleep 1
}
