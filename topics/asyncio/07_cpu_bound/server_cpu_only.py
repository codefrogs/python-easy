#!/usr/bin/env python3

# Shows just the primer calculator in its own process.

import logging
import socket
import asyncio
import signal
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value
from prime_calculator import PrimeCalculator
from enum import Enum, auto
from typing import Optional
import time


prime: Optional[Value] = None


def run_prime_search(max):
    global prime
    print("Searching primes...")
    prime_calculator = PrimeCalculator()
    run = 0
    while (run != max):
        time.sleep(1)
        prime_calculator.find_next()
        with prime.get_lock():
            prime.value = prime_calculator.get_latest()
        print(".")
        run +=1

async def run_prime_task(pool):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(pool, run_prime_search, 60)    

def init_global(shared_prime):
    global prime
    prime = shared_prime

async def main():
    global prime 
    prime = Value('i', 0) # We declare an integer with value zero.
    
    try:
        with ProcessPoolExecutor(initializer=init_global, initargs=(prime,)) as pool:
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
