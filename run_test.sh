#!/bin/bash
set -e


current_time=$(date "+%Y%m%d_%H%M%S")
g_directory="/mnt/stateful_partition/results/$current_time"
python3 ./run.py -H $1 -d $g_directory $2
rm -rf $g_directory/test_file
./generate_result.sh $g_directory $2
