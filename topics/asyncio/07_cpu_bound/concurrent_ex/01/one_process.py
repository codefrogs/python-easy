#!/usr/bin/env python3

# This is taken from the python documentation:
# https://docs.python.org/3/library/multiprocessing.html#the-process-class

from multiprocessing import Process

def cpu_func(name):
    print('hello', name)

if __name__ == '__main__':
    p = Process(target=cpu_func, args=('world!',))
    p.start()
    p.join()