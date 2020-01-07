#!/usr/bin/python3

import subprocess
import sys
import getopt, sys

GBK = 'gbk'
UTF8 = 'utf-8'
current_encoding = UTF8 


class Case:
	bin_case=""
	file_testlog="test.log"
	file_testlog=""
	file_turbostatlog=""

	def __init__(self, bin_case, file_testlog):
		self.bin_case = bin_case
		self.file_testlog = file_testlog

		self.file_testlog= open(file_testlog, "w")
		self.file_turbostatlog = open("turbostat.log", "w")
 
		self.do_run()

	def do_run(self):
		p_turbostat = subprocess.Popen(['/home/chrome/linux/tools/power/x86/turbostat/turbostat -s PkgWatt,CorWatt,GFXWatt,RAMWatt'],
			shell=True,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			bufsize=1)
		
		p_test = subprocess.Popen([self.bin_case],
		 	shell=True,
		 	stdout = subprocess.PIPE,
		 	stderr = subprocess.PIPE,
		 	bufsize=1)
		
		while p_test.poll() is None:
		    r = p_test.stdout.readline().decode(current_encoding)
		    sys.stdout.write(r)
		    self.file_testlog.write(r)
		    self.file_testlog.flush()
		
		    r = p_turbostat.stdout.readline().decode(current_encoding)
		    sys.stdout.write(r)
		    self.file_turbostatlog.write(r)
		    self.file_turbostatlog.flush()
		
		
		if p_test.poll() != 0: 
		    err = p_test.stderr.read().decode(current_encoding)
		    sys.stdout.write(err)
		    self.file_testlog.write(err)
		    self.file_testlog.flush()
		
		self.file_testlog.close()
		self.file_turbostatlog.close()


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
	case1 = Case("ping 127.0.0.1 -c 15", "test.log")

	######## Add test cases here! #############


if __name__ == "__main__":
    main()

