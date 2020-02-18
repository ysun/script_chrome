# script_chromesudo
This is a simple automated test framework for ChromeOS and Linux VM

## Install
There're some dependencies as followed

`sudo apt install python3-pip`
`sudo pip3 install paramiko`
`sudo apt install fio`

## Usage
usage: run.py [-h] [-d DIRECTORY] [-c] [-g] [-H IP_HOST] [-G IP_GUEST]
              [-t [TEST_CASES]] [-p CASE_PATTERN]
              {host,guest} ...

positional arguments:
  {host,guest}
    host                Run this test framework on a host machine
    guest               Run this test framework on a VM

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The directory for saving results and logs. Default is
                        /mnt/statefule_partation/<current_dateime>
  -c, --max-cpu         Online all CPU cores, only 2 out of 4 cores are
                        enabled by default on Pixelbook; And force cpus
                        running at highest freq!
  -g, --max-gpu         Force GPU running with highest freqency!
  -H IP_HOST, --host-ip IP_HOST
                        Specify IP of host side, default is 100.115.92.25
                        which is default value of pixelbook
  -G IP_GUEST, --guest-ip IP_GUEST
                        Specify IP of guest side, which is random, have to be
                        given
  -t [TEST_CASES], --test-case [TEST_CASES]
                        Specify test cases list
  -p CASE_PATTERN, --case-pattern CASE_PATTERN
                        Specify test cases pattern string
## Some other tools
### max_cpu.sh
Force enable all 4 cores and setup all cores running on the Max frequency.

### max_gpu.sh
Force GPU running on the Max frequency.

### top_cpu.sh
Dump cpu runncing frequency

### setup_env.sh
Setup test environment for ChromeOS. It should be run on host only.
