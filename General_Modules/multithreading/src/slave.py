__author__ = 'zhuhy'

import sys


def create_log(arg1, arg2):
    """
    Manage log file
    :param arg1: lower bound
    :param arg2: upper bound
    :return: File pointer
    """
    f = open(arg1 + "_" + arg2 + ".log", "w")
    return f


def func_square(file, arg3):
    """
    Executable functions
    :param file: Output file
    :param arg3: Input argument
    :return: whatever
    """
    file.write(str(int(arg3)**2))
    file.close()


def main():
    """
    Executable body, call other functions from here
    :return: Exit code
    """
    print('Number of arguments: ' + str(len(sys.argv)) + " arguments.")
    print('List of arguments:' + str(sys.argv))
    f = create_log(sys.argv[1], sys.argv[2])
    func_square(f, sys.argv[3])

if __name__ == "__main__":
    main()
