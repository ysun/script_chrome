#! /bin/bash

echo "Please to open adb"
echo "starting test android fio..."
adb push /mnt/stateful_partition/Storage_FIO/fio /data/local/tmp/
adb shell /data/local/tmp/fio -direct=1 -ioengine=libaio -size=512M -numjobs=4 -name=/data/local/tmp/fio_read --group_reporting --runtime=600 --bs=4k -rw=read

adb shell /data/local/tmp/fio -direct=1 -ioengine=libaio -size=512M -numjobs=4 -name=/data/local/tmp/fio_write --group_reporting --runtime=600 --bs=4k -rw=write

adb shell /data/local/tmp/fio -direct=1 -ioengine=libaio -size=512M -numjobs=4 -name=/data/local/tmp/fio_randread --group_reporting --runtime=600 --bs=4k -rw=randread

adb shell /data/local/tmp/fio -direct=1 -ioengine=libaio -size=512M -numjobs=4 -name=/data/local/tmp/fio_randwrite --group_reporting --runtime=600 --bs=4k -rw=randwrite
adb shell rm -rf /data/local/tmp/fio_*
sleep 5
echo "done"

echo "starting test android geekbench..."
adb push /mnt/stateful_partition/Geekbench-5.3.0-Android-Corporate/* /data/local/tmp/
adb shell /data/local/tmp/geekbench_x_86_64 --unlock geekbench@intel.com LBLOH-LDXXG-EOTSO-CMU7C-4W225-R6YP5-M7TEI-7CCNR-UXYDE
adb shell /data/local/tmp/geekbench_x86_64 --no-upload --cpu
