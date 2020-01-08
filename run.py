#!/usr/bin/python3

import subprocess
import sys,os
import getopt, sys

import argparse

GBK = 'gbk'
UTF8 = 'utf-8'
current_encoding = GBK

g_directory="/mnt/stateful_partition/results/"

class Case:
	bin_case=""
	file_testlog="test.log"
	file_turbostatlog="turbostat.log"

	def __init__(self, bin_case, file_testlog, file_turbostatlog):
		self.bin_case = bin_case
		self.file_testlog = file_testlog
		self.file_turbostatlog = file_turbostatlog

		self.file_testlog = open(file_testlog, "w")
#		self.file_turbostatlog = open(file_turbostatlog, "w")
 
		self.do_run()

	def do_run(self):
		p_turbostat = subprocess.Popen(['turbostat -s PkgWatt,CorWatt,GFXWatt,RAMWatt -q -i 1 -o %s'%self.file_turbostatlog],
			shell=True)
# Do not handle stdout/errout of turbostat
# Use its output augument instead.
#			stdout = subprocess.PIPE,
#			stderr = subprocess.PIPE,
#			bufsize=1)
		
		print("[Running]: %s"%self.bin_case)
		p_test = subprocess.Popen([self.bin_case],
		 	shell=True,
		 	stdout = subprocess.PIPE,
		 	stderr = subprocess.PIPE,
		 	bufsize=0)
		
		while p_test.poll() is None:
		    std_out = p_test.stdout.read().decode(current_encoding)
		    self.file_testlog.write(std_out)
#		    sys.stdout.write(std_out)
		    self.file_testlog.flush()
		
# Do not handle stdout/errout of turbostat
# Use its output augument instead.
#		    r = p_turbostat.stdout.readline().decode(current_encoding)
#		    self.file_turbostatlog.write(r)
#		    self.file_turbostatlog.flush()
#		    sys.stdout.write(r)

		if p_test.poll() != 0: 
		    err = p_test.stderr.read().decode(current_encoding)
		    sys.stdout.write(err)
		    self.file_testlog.write(err)
		    self.file_testlog.flush()
		
		self.file_testlog.close()
		print("[Done]")
#		self.file_turbostatlog.close()

def main():
	try:
            opts, args = getopt.getopt(sys.argv[1:], "d:r:h", ["directory", "run", "help"])
	except getopt.GetoptError as err:
		print(err)  # will print something like "option -a not recognized"
#		usage()
		sys.exit(2)
	output = None
	verbose = False
	for o, a in opts:
		if o in ("-r", "--run"):
			bin_case=a
			print(a)
		elif o in ("-h", "--help"):
			print("usage()")
			sys.exit()
		elif o in ("-d", "--directory"):
                    global g_directory
                    g_directory = a

                    if not os.path.exists(g_directory):
                            os.makedirs(g_directory)

		else:
			assert False, "unhandled option"

	run_cases()


def run_cases():
	######## Add test cases here! #############
#	case1 = Case("ping 127.0.0.1 -c 15", "test.log")

	case1 = Case("fio -filename=%s/test_file -direct=1 -iodepth 256 -rw=read -ioengine=libaio -size=2G -numjobs=2 -name=fio_read"%g_directory, "%s/fio_read.log"%g_directory, "%s/turbostat_read.log"%g_directory)
	case2 = Case("fio -filename=%s/test_file -direct=1 -iodepth 256 -rw=write -ioengine=libaio -size=2G -numjobs=2 -name=fio_write"%g_directory, "%s/fio_write.log"%g_directory, "%s/turbostat_write.log"%g_directory)
	case3 = Case("fio -filename=%s/test_file -direct=1 -iodepth 256 -rw=randread -ioengine=libaio -size=2G -numjobs=2 -name=fio_randread"%g_directory, "%s/fio_randread.log"%g_directory, "%s/turbostat_randread.log"%g_directory)
	case4 = Case("fio -filename=%s/test_file -direct=1 -iodepth 256 -rw=randwrite -ioengine=libaio -size=2G -numjobs=2 -name=fio_randwrite"%g_directory, "%s/fio_randwrite.log"%g_directory, "%s/turbostat_randwrite.log"%g_directory)
	case5 = Case("iperf3 -c 127.0.0.1 -t 60 -i 60", "%s/iperf3.log"%g_directory, "%s/turbostat_iperf3.log"%g_directory)
	case6 = Case("netperf -H 127.0.0.1 -t tcp_stream -l 60", "%s/netperf_stream.log"%g_directory, "%s/turbostat_netperf_stream.log"%g_directory)
	case7 = Case("netperf -H 127.0.0.1 -t tcp_rr -l 20", "%s/netperf_rr.log"%g_directory, "%s/turbostat_netperf_rr.log"%g_directory)


if __name__ == "__main__":
    main()

