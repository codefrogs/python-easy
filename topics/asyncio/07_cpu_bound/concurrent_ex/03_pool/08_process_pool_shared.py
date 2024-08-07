#!/usr/bin/env python3

from multiprocessing import Process
from multiprocessing import Value
from concurrent.futures import ProcessPoolExecutor

import time

def count(sum, max):
    with sum.get_lock():
        for i in range(max):
            sum.value += 1               
    return sum

def main():
    COUNT_MAX=20
    sum = Value('i', 0) # We declare an integer with value zero.
    
    with ProcessPoolExecutor() as pool:
      future_object = pool.submit(count, sum, COUNT_MAX) # One process      
      counted = future_object.result() # blocks until we get the result.

    print(f"Total: {sum.value}")

    # This does not work at all!
    # Notice the error messages contain: obj = _ForkingPickler.dumps(obj)
    # The pool is trying to serialise the shared memory object.
    # This does not work. Let's fix this.
    
if __name__ == "__main__":
    main()
