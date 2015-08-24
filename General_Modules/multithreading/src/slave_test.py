__author__ = 'zhuhy'

import sys
import time
import random


def create_log(arg1, arg2):
    """
    Manage log file
    :param arg1: lower bound
    :param arg2: upper bound
    :return: File pointer
    """
    f = open(arg1 + "_" + arg2 + "_out.log", "w")
    g = open(arg1 + "_" + arg2 + ".log", "w")
    g.write('Number of arguments: ' + str(len(sys.argv)) + " arguments.\n")
    g.write('List of arguments:' + str(sys.argv) + "\n")
    return f, g


def func(file1, file2):
    """
    Executable functions
    :param file: Output file
    :param arg3: Input argument
    :return: whatever
    """
    file1.write(str(sys.argv[2]))
    file1.close()
    # sec = 20 - int(int(sys.argv[1])/2000)
    sec = int(20 * random.random())
    time.sleep(sec)
    file2.write("I slept for %d seconds.\n" % sec)
    file2.close()


def main():
    """
    Executable body, call other functions from here
    :return: Exit code
    """
    f, g = create_log(sys.argv[1], sys.argv[2])
    func(f, g)

if __name__ == "__main__":
    main()
