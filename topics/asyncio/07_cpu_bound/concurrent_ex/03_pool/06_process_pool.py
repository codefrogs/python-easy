#!/usr/bin/env python3

from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
import time

def count(val):
    sum = 0
    for i in range(val):
        sum += 1
        time.sleep(1)
    return sum

def main():
    COUNT_MAX=20
    
    with ProcessPoolExecutor() as pool:
      future_object = pool.submit(count, COUNT_MAX) # One process      
      counted = future_object.result() # blocks until we get the result.

    print(f"Total: {counted}")

    # This is OK as it is, but we want to get constant updates about our count.
    # So let's introduce a shared counter object.

if __name__ == "__main__":
    main()
