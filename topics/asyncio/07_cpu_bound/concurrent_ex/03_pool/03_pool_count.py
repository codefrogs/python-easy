#!/usr/bin/env python3

from multiprocessing import Pool
import time

def count(val):
    sum = 0
    for i in range(val):
        sum += 1

def count_timed(val):
    start = time.time()
    count(val)
    end = time.time()

    elapsed = end - start
    return elapsed


def main():
    # We will run our count function directly and in a process.
    COUNT_MAX=1000000

    with Pool(1) as pool:
      print("Pool created")

      print("1. Blocking process")
      result = pool.apply(func=count_timed, args=(COUNT_MAX,))

    print(f"Time elapsed: {result}")

if __name__ == "__main__":
    main()
