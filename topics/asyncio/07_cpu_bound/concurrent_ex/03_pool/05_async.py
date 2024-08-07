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
    COUNT_MAX=10000000

    # Now lets try two processes, with pool
    with Pool() as pool:
      print("1. Two processes")
      start_time = time.time()
      result1 = pool.apply_async(func=count_timed, args=(COUNT_MAX,))
      result2 = pool.apply_async(func=count_timed, args=(COUNT_MAX,))

      elapsed1 = result1.get() # blocks until we get the result
      elapsed2 = result2.get() # also blocks.

      end_time = time.time()

    elapsed = end_time - start_time

    print(f"2. Count(1) elapsed: {elapsed1}")
    print(f"3. Count(2) elapsed: {elapsed2}")
    print()
    print("4. Total duration", elapsed)
    print("5. Average duration", elapsed/2)

    # So running two processes in a pool, we get a speed increase.
    # Both take about the same time to execute, but the average
    # for both is half.

if __name__ == "__main__":
    main()
