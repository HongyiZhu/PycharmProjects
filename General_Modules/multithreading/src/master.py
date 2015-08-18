__author__ = 'zhuhy'

import subprocess
import time

# Global Configuration
python_path = "C:/Python34/python.exe"
slave_path = "C:/Users/zhuhy/Documents/GitHub/PycharmProjects/General_Modules/multithreading/src/slave.py"

# Modify iterange according to the need
overall_scale = 10000
slice_size = 100
iterange = 0

for iter in range(iterange):
    # Append parameters into the args list
    args = [python_path, slave_path]
    for i in range(1,4):
        args.append('%s' % str(i))

    # Subprocess the slaves.
    proc = subprocess.Popen(args)
    while proc.poll() == None:
        time.sleep(1)