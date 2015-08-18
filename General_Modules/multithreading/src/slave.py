__author__ = 'zhuhy'

import sys

def create_log(arg1, arg2):
    f = open(arg1 + "_" + arg2 + ".log", "w")
    return f

def func_square(file, arg3):
    file.write(str(int(arg3)**2))
    file.close()

def main():
    print('Number of arguments: ' + str(len(sys.argv)) + " arguments.")
    print('List of arguments:' + str(sys.argv))
    f = create_log(sys.argv[1], sys.argv[2])
    func_square(f, sys.argv[3])

if __name__ == "__main__":
    main()