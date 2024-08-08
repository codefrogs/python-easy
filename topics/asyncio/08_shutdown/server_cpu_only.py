#!/usr/bin/env python3

# Shows just the primer calculator in its own process.

import logging
import asyncio
import signal
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value
from prime_calculator import PrimeCalculator
from enum import Enum, auto
from typing import Optional
import time

prime: Optional[Value] = None
running: Optional[Value] = None

def run_prime_search():
    global prime
    global running
    print("Searching primes...")
    prime_calculator = PrimeCalculator()
    run = 0
    while (running.value):
        time.sleep(1)
        prime_calculator.find_next()
        with prime.get_lock():
            prime.value = prime_calculator.get_latest()
        print(".", flush=True, end='')
        run +=1
    print("Search stopped.")

async def run_prime_task(pool):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(pool, run_prime_search)    

def init_global(shared_prime, shared_running):
    global prime
    global running
    prime = shared_prime
    running = shared_running

def shutdown():
    global running
    if running.value == 0: # Nothing to do for this process in the pool
        return
    print("\nShutdown called!")
    
    with running.get_lock():
        running.value = 0

async def main():
    global prime
    global running

    running = Value('B', True)
    prime = Value('i', 0) # We declare an integer with value zero.

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)

    try:
        with ProcessPoolExecutor(initializer=init_global, initargs=(prime,running)) as pool:            
            
            prime_task = asyncio.create_task(run_prime_task(pool), name="task_prime")
        
            await prime_task

        print("Server finished.")

    except asyncio.CancelledError as e:        
        print("Server cancelled.")

    except Exception as e:
        logging.exception(e)
        print("Terminated.")

if __name__ == "__main__":
    asyncio.run(main())
