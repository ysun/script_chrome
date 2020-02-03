#!/bin/bash
#set -x
set -e

intel_gpu_frequency -m
echo "Now GPU frequency is: `intel_gpu_frequency -g`" 
