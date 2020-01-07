#!/usr/local/bin/python3

import subprocess
import sys


GBK = 'gbk'
UTF8 = 'utf-8'
current_encoding = UTF8 

file_testlog= open("test.log", "w")
file_turbostlog = open("turbost.log", "w")
 
p_turbost = subprocess.Popen(['turbost -s PkgWatt,CorWatt,GFXWatt,RAMWatt '],
	shell=True,
	stdout = subprocess.PIPE,
	stderr = subprocess.PIPE,
	bufsize=1)

p_test = subprocess.Popen(['ping 127.0.0.1 -c 3'],
	shell=True,
	stdout = subprocess.PIPE,
	stderr = subprocess.PIPE,
	bufsize=1)

while p_test.poll() is None:
    r = p_test.stdout.readline().decode(current_encoding)
    sys.stdout.write(r)
    file_testlog.write(r)
    file_turbostlog.flush()

    r = p_turbost.stdout.readline().decode(current_encoding)
    sys.stdout.write(r)
    file_turbostlog.write(r)
    file_turbostlog.flush()


if p_test.poll() != 0: 
    err = p_test.stderr.read().decode(current_encoding)
    sys.stdout.write(err)
    file_testlog.write(err)
    file_testlog.flush()
