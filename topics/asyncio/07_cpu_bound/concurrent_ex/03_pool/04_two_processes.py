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
    print("Elaped time:", elapsed, "s")
    return elapsed


def main():
    # We will run our count function directly and in a process.
    COUNT_MAX=10000000

    # Now lets try two processes, with pool
    with Pool() as pool:
      print("1. Two processes")
      start_time = time.time()
      result1 = pool.apply(func=count_timed, args=(COUNT_MAX,))
      result2 = pool.apply(func=count_timed, args=(COUNT_MAX,))
      end_time = time.time()

    elapsed = end_time - start_time
    print("2. Total duration", elapsed)
    print("3. Average duration", elapsed/2)

    # So running two processes in a pool, we do *not* get a speed increase.

if __name__ == "__main__":
    main()
