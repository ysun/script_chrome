#!/bin/bash
set -x

for((i=0; i<4; i++)) {
	echo 1 > /sys/devices/system/cpu/cpu${i}/online
	echo performance > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_governor

	cat /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_max_freq > /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_min_freq
}
