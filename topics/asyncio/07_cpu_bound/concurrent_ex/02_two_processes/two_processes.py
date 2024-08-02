#!/usr/bin/env python3

from multiprocessing import Process
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
    print("1. Direct call")
    elapsed_single = count_timed(COUNT_MAX)

    print("2. One process")
    p = Process(target=count_timed, args=(COUNT_MAX,)) # Don't forget the comma!
    p.start()
    p.join()

    # Now lets try two processes
    print("3. Two processes")
    start_time = time.time()
    p1 = Process(target=count_timed, args=(COUNT_MAX,))
    p2 = Process(target=count_timed, args=(COUNT_MAX,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end_time = time.time()

    elapsed = end_time - start_time
    print("6. Total duration", elapsed)
    print("7. Average duration", elapsed/2)

    # So with two processes, we get a speed increase!

if __name__ == "__main__":
    main()
