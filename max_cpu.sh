#!/bin/bash
#set -x
set -e

for((i=1; i<4; i++)) {
	echo 1 > /sys/devices/system/cpu/cpu${i}/online
	echo "Force cpu${i} online, now is `cat /sys/devices/system/cpu/cpu${i}/online`"
	sleep 1

	echo performance > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_governor
	echo "Force cpu${i} performance, now is `cat /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_governor`"
	sleep 1

	cat /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_max_freq > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_min_freq
	echo "Force cpu${i} max frequency, now is `cat /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_cur_freq`"
	sleep 1
}
