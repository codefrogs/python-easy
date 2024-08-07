#!/usr/bin/env python3

from multiprocessing import Process
from multiprocessing import Value
from concurrent.futures import ProcessPoolExecutor

import time

def count(sum, val):
    with sum.get_lock():
        #sum.get_lock().acquire() 
        for i in range(val):
            sum.value += 1       
        #sum.get_lock().release()  
    return sum

def main():
    COUNT_MAX=20
    sum = Value('i', 0) # We declare an integer with value zero.
    
    p1 = Process(target=count, args=(sum, COUNT_MAX,))
    p2 = Process(target=count, args=(sum, COUNT_MAX,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(f"Total: {sum.value}")

    # This works. We get a total of 20.
    # Let's now do the same with ProcessPoolExecutor
    
    
if __name__ == "__main__":
    main()
