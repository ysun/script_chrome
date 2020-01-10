#!/usr/bin/python3

import subprocess
import sys,os
import getopt, sys

import argparse
 
import signal
import re


GBK = 'gbk'
UTF8 = 'utf-8'
current_encoding = GBK

g_directory="/mnt/stateful_partition/results/"
g_results_list = dict()

def signal_handler(sig, frame):
	print('Interruptted by user! (Ctrl+C)')
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


class Case:
	bin_case=""
	case_name=""
	file_testlog="test.log"
	file_turbostatlog="turbostat.log"
	result=""

	output_std=""

	def __init__(self, case_name, bin_case, file_testlog, file_turbostatlog):
		self.case_name = case_name
		self.bin_case = bin_case
		self.file_testlog = file_testlog
		self.file_turbostatlog = file_turbostatlog

		self.file_testlog = open(file_testlog, "w")
#		self.file_turbostatlog = open(file_turbostatlog, "w")
 
		self.do_run()

	def result_parser(self, pattern, line_num=0):
		if line_num != 0:
			stdout = self.output_std.splitlines()[line_num]
		else:
			stdout = self.output_std

		try:
			ret = re.search(pattern, stdout).group(1)
		except:
			ret = None

			print(self.output_std)
			print(pattern)
			print(stdout)

		return ret

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
		    self.output_std = std_out

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
		p_turbostat.kill()
		print("[Done]")
#		self.file_turbostatlog.close()

def main():
	parser = argparse.ArgumentParser(description='This is a simple automated test framework for ChromeOS and Linux VM')
	parser.add_argument('-d','--directory',
		help='The directory for saving results and logs',
		default='/mnt/stateful_partition/results/')

	args = parser.parse_args()

	global g_directory
	g_directory = getattr(args, 'directory')

	if not os.path.exists(g_directory):
		os.makedirs(g_directory)

	run_cases()
	print(g_results_list)

	for key,value in g_results_list.items():
		print('%s %s'%(key,value))

def run_cases():
	######## Add test cases here! #############
	case = Case("fio-read", "fio -filename=%s/test_file -direct=1 -iodepth 256 -rw=read -ioengine=libaio -size=2G -numjobs=2 -name=fio_read"%g_directory, "%s/fio_read.log"%g_directory, "%s/turbostat_read.log"%g_directory)
	g_results_list[case.case_name] = case.result_parser(r'READ: \S* \((\S*)MB/s\)', 0)

	case = Case("fio-write", "fio -filename=%s/test_file -direct=1 -iodepth 256 -rw=write -ioengine=libaio -size=2G -numjobs=2 -name=fio_write"%g_directory, "%s/fio_write.log"%g_directory, "%s/turbostat_write.log"%g_directory)
	g_results_list[case.case_name] = case.result_parser(r'WRITE: \S* \((\S*)MB/s\)', 0)

	case = Case("fio-randread", "fio -filename=%s/test_file -direct=1 -iodepth 256 -rw=randread -ioengine=libaio -size=2G -numjobs=2 -name=fio_randread"%g_directory, "%s/fio_randread.log"%g_directory, "%s/turbostat_randread.log"%g_directory)
	g_results_list[case.case_name] = case.result_parser(r'READ: \S* \((\S*)MB/s\)', 0)

	case = Case("fio-randwrite", "fio -filename=%s/test_file -direct=1 -iodepth 256 -rw=randwrite -ioengine=libaio -size=2G -numjobs=2 -name=fio_randwrite"%g_directory, "%s/fio_randwrite.log"%g_directory, "%s/turbostat_randwrite.log"%g_directory)
	g_results_list[case.case_name] = case.result_parser(r'WRITE: \S* \((\S*)MB/s\)', 0)

	case = Case("iperf3", "iperf3 -c 127.0.0.1 -t 60 -i 60", "%s/iperf3.log"%g_directory, "%s/turbostat_iperf3.log"%g_directory)
	g_results_list[case.case_name] = case.result_parser(r'.* (\S*) Gbits/sec.*receiver', 0)

	case = Case("netperf-tcp_stream", "netperf -H 127.0.0.1 -t tcp_stream -l 60", "%s/netperf_stream.log"%g_directory, "%s/turbostat_netperf_stream.log"%g_directory)
	g_results_list[case.case_name] = case.result_parser(r'.* (\S*)$', 6)

	case = Case("netperf-rr", "netperf -H 127.0.0.1 -t tcp_rr -l 20", "%s/netperf_rr.log"%g_directory, "%s/turbostat_netperf_rr.log"%g_directory)
	g_results_list[case.case_name] = case.result_parser(r'.* (\S*)$', 6)


if __name__ == "__main__":
    main()
