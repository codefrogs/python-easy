#!/usr/bin/env python3

# Async prime server example: cleaned up
#
import logging
import asyncio
import signal
import time

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value
from typing import Optional
from step_09 import PrimeServerAsync
from step_09 import PrimeCalculator
from step_09 import globals

server: Optional[PrimeServerAsync] = None


class PrimeApp:

    def init(self):
        self.init_shares()
        self.create_prime_server()

    def init_shares(self):
        globals.prime = Value('i', 0)  # We declare an integer with value zero.
        globals.running = Value('B', 1)  # We declare an integer with value zero.

    def create_prime_server(self):
        global server
        server = PrimeServerAsync()


def run_prime_search(max):
    prime_calculator = PrimeCalculator()
    prime_calculator.run()


async def run_prime_task(pool):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(pool, run_prime_search, 60)


def create_prime_task(pool):
    return asyncio.create_task(run_prime_task(pool), name="task_prime")


def copy_globals_to_process(shared_prime, shared_running):
    globals.prime = shared_prime
    globals.running = shared_running


async def run_server():
    global server
    with ProcessPoolExecutor(initializer=copy_globals_to_process,
                             initargs=(globals.prime, globals.running),
                             max_workers=1) as pool:
        prime_task = create_prime_task(pool)
        server_task = server.run()
        await asyncio.gather(prime_task, server_task)


def cancel_all(tasks):
    for t in tasks:
        t.cancel()


def cancel_prime_calc_task(tasks):
    for t in tasks:
        if t.get_name() == "prime_task":
            t.cancel()
            tasks.remove(t)  # Doing more than one thing! OHOH FIXME!


def pause_one_second():
    time.sleep(1)


def set_running_to_false():
    with globals.running.get_lock():
        globals.running.value = 0
        print(f"running: {globals.running.value}", flush=True)


def cancel_server():
    print("\nShutting down...")

    set_running_to_false()
    server.cancel()

    pause_one_second()  # Give any process, and task a chance to stop

    tasks = asyncio.all_tasks()
    cancel_prime_calc_task(tasks)
    cancel_all(tasks)


def is_running():    
    return globals.running.value == 1


def shutdown():
    if is_running():  # Nothing to do for this process in the pool
        cancel_server()


def add_interrupt_handler():
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)


async def main():

    app = PrimeApp()
    app.init()

    # init_shares()
    # create_prime_server()
    add_interrupt_handler()

    try:
        await run_server()
        print("Server finished.")

    except asyncio.CancelledError:
        print("Server cancelled.")

    except Exception as e:
        logging.exception(e)
        print("Terminated.")

    # That's it for now!

if __name__ == "__main__":
    asyncio.run(main())
