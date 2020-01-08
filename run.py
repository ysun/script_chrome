#!/usr/bin/python3

import subprocess
import sys
import getopt, sys

GBK = 'gbk'
UTF8 = 'utf-8'
current_encoding = GBK


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
#			stdout = subprocess.PIPE,
#			stderr = subprocess.PIPE,
#			bufsize=1)
		
		p_test = subprocess.Popen([self.bin_case],
		 	shell=True,
		 	stdout = subprocess.PIPE,
		 	stderr = subprocess.PIPE,
		 	bufsize=0)
		
		while p_test.poll() is None:
		    std_out = p_test.stdout.read().decode(current_encoding)
		    self.file_testlog.write(std_out)
		    sys.stdout.write(std_out)

		    err_out = p_test.stderr.read().decode(current_encoding)
		    self.file_testlog.write(err_out)
		    sys.stdout.write(err_out)

		    self.file_testlog.flush()
		
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
#		self.file_turbostatlog.close()


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "r:h", ["run", "help"])
	except getopt.GetoptError as err:
		# print help information and exit:
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
		else:
			assert False, "unhandled option"

	run_cases()


def run_cases():
	######## Add test cases here! #############
#	case1 = Case("ping 127.0.0.1 -c 15", "test.log")

	case1 = Case("fio -filename=/mnt/stateful_partition/test_file -direct=1 -iodepth 256 -rw=read -ioengine=libaio -size=2G -numjobs=2 -name=fio_read", "/mnt/stateful_partition/fio_read.log", "/mnt/stateful_partition/turbostat_read.log")
	case2 = Case("fio -filename=/mnt/stateful_partition/test_file -direct=1 -iodepth 256 -rw=write -ioengine=libaio -size=2G -numjobs=2 -name=fio_write", "/mnt/stateful_partition/fio_write.log", "/mnt/stateful_partition/turbostat_write.log")
	case3 = Case("fio -filename=/mnt/stateful_partition/test_file -direct=1 -iodepth 256 -rw=randread -ioengine=libaio -size=2G -numjobs=2 -name=fio_randread", "/mnt/stateful_partition/fio_randread.log", "/mnt/stateful_partition/turbostat_randread.log")
	case4 = Case("fio -filename=/mnt/stateful_partition/test_file -direct=1 -iodepth 256 -rw=randwrite -ioengine=libaio -size=2G -numjobs=2 -name=fio_randwrite", "/mnt/stateful_partition/fio_randwrite.log", "/mnt/stateful_partition/turbostat_randwrite.log")
	case5 = Case("iperf3 -c 127.0.0.1 -t 60 -i 60", "/mnt/stateful_partition/iperf.log", "/mnt/stateful_partition/turbostat_iperf.log")
	case6 = Case("netperf -H 127.0.0.1 -t tcp_stream -l 60", "/mnt/stateful_partition/netperf_stream.log", "/mnt/stateful_partition/turbostat_netperf_stream.log")
	case7 = Case("netperf -H 127.0.0.1 -t tcp_rr -l 20", "/mnt/stateful_partition/netperf_rr.log", "/mnt/stateful_partition/turbostat_netperf_rr.log")


if __name__ == "__main__":
    main()

