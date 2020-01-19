#!/bin/bash
#set -x
set -e

while [ True ];
do
	freq=`intel_gpu_frequency -g | grep cur | cut -d" " -f2`
	echo $freq
	sleep 1
done
