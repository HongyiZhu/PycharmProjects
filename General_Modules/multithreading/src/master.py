__author__ = 'zhuhy'

import subprocess
import os
import time

# Global Configuration
python_path = "C:/Python34/python.exe"
# slave_path = "C:/Users/zhuhy/Documents/GitHub/PycharmProjects/General_Modules/multithreading/src/slave.py"
slave_path = "C:/Users/Hongyi/Documents/GitHub/PycharmProjects/General_Modules/multithreading/src/"
os.chdir(slave_path)

script_name = "slave_test.py"

# Modify iterange according to the need
overall_scale = 9999
slice_size = 2000

# A list to record slice argument information
args_list = []
for i in range(1, overall_scale, slice_size):
    args = [python_path, script_name]
    if i + slice_size < overall_scale:
        args.append(str(i))
        args.append(str(i + slice_size - 1))
    else:
        args.append(str(i))
        args.append(str(overall_scale))
    args_list.append(args)

# Initiate a list of subprocess
proc_list = []
proc_status_list = []
for args in args_list:
    proc_list.append(subprocess.Popen(args))
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
    for i in range(0, len(proc_status_list), 10):
        print("\t".join(str(v) for v in proc_status_list[i: i + 10]))
    print("===================================")
    if 1 in proc_status_list:
        time.sleep(5)
    else:
        break

print("All child processes are finished!")






