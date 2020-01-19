#!/bin/bash
#set -x
set -e

while [ True ]
do
	for((i=0; i<4; i++)) {
		cpu_freq[$i]=`cat /sys/devices/system/cpu/cpu${i}/cpufreq/scaling_cur_freq`
	}
	
	for((i=0; i<4; i++)) {
		echo -n ${cpu_freq[$i]}" "
	}
	echo
sleep 1
done
