__author__ = 'zhuhy'

import subprocess
import os
import time
from subprocess import PIPE


def new_mod(a):
    if a < 13:
        return a
    else:
        return 13

# Global Configuration
python_path = "python3"
# slave_path = "C:/Users/zhuhy/Documents/GitHub/PycharmProjects/General_Modules/multithreading/src/slave.py"
slave_path = "/home/sagars/"
os.chdir(slave_path)

script_name = "slave_zmap.py"

# Modify iterange according to the need
overall_scale = 1000
slice_size = 2

# A list to record slice argument information
args_list = []
for i in range(0, overall_scale, slice_size):
    args = [python_path, script_name]
    if i + slice_size <= overall_scale:
        args.append(str(i + 1))
        args.append(str(i + slice_size))
    else:
        args.append(str(i + 1))
        args.append(str(overall_scale))
    args_list.append(args)

# Initiate a list of subprocess
proc_list = []
proc_status_list = []
for args in args_list:
    proc_list.append(subprocess.Popen(args, stdout=PIPE,stderr=PIPE))
    proc_status_list.append(1)
print("%s subprocess started!" % str(len(proc_status_list)))
print("======================")

while 1 in proc_status_list:
    for i in range(len(proc_status_list)):
        if proc_status_list[i] == 1:
            proc = proc_list[i]
            flag = proc.poll()
            if flag is not None:
                proc_status_list[i] = 0
    print("Checking child process status:")
    for i in range(0, len(proc_status_list), 13):
        print("\t".join(str(v) for v in proc_status_list[i: i + 13]))
    print("="*(8*(new_mod(len(proc_list)))-7))
    if 1 in proc_status_list:
        time.sleep(20)
    else:
        break

print("All child processes are finished!")






