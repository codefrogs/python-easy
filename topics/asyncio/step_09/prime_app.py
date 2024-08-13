#!/usr/bin/env python3

# Async prime server example: cleaned up
#
import logging
import asyncio
import signal
import time

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value

from step_09 import PrimeServerAsync
from step_09 import PrimeCalculator
from step_09 import globals


prime_calculator = None


class InterruptHandler:

    def __init__(self, server):
        self.server = server

    def init(self):
        self.add_interrupt_handler()

    def add_interrupt_handler(self):
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, self.shutdown)

    def shutdown(self):
        if self.is_running():  # Nothing to do for this process in the pool
            self.cancel_server()

    def is_running(self):
        return globals.prime_running.value == 1

    def cancel_server(self):
        # global server
        print("\nShutting down...")

        self.set_running_to_false()
        self.server.cancel()

        self.pause_one_second()  # Give any process, and task a chance to stop

        tasks = asyncio.all_tasks()
        self.cancel_prime_calc_task(tasks)
        self.cancel_all(tasks)

    def set_running_to_false(self):
        with globals.prime_running.get_lock():
            globals.prime_running.value = 0
            print(f"running: {globals.prime_running.value}", flush=True)

    def pause_one_second(self):
        time.sleep(1)

    def cancel_prime_calc_task(self, tasks):
        for t in tasks:
            if t.get_name() == "prime_task":
                t.cancel()
                tasks.remove(t)

    def cancel_all(self, tasks):
        for t in tasks:
            t.cancel()


def init_shares():
    globals.prime = Value('i', 0)
    globals.prime_running = Value('B', 1)


def create_prime_server():
    return PrimeServerAsync()


def copy_globals_to_process(shared_prime, shared_running):
    globals.prime = shared_prime
    globals.prime_running = shared_running


def create_prime_calculator():
    global prime_calculator
    prime_calculator = PrimeCalculator()


def run_prime_search():
    prime_calculator.run()


async def run_tasks(server):

    with ProcessPoolExecutor(initializer=copy_globals_to_process,
                             initargs=(globals.prime, globals.prime_running),
                             max_workers=1) as pool:

        prime_task = create_prime_task(pool)
        server_task = server.run()

        await asyncio.gather(prime_task, server_task)


def create_prime_task(pool):
    return asyncio.create_task(run_prime_task(pool), name="task_prime")


async def run_prime_task(pool):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(pool, run_prime_search)


async def main():
    init_shares()
    server = create_prime_server()
    create_prime_calculator()

    interrupt_handler = InterruptHandler(server)
    interrupt_handler.init()

    try:
        await run_tasks(server)
        print("Server finished.")

    except asyncio.CancelledError:
        print("Server cancelled.")

    except Exception as e:
        logging.exception(e)
        print("Terminated.")

    # That's it for now!

if __name__ == "__main__":
    asyncio.run(main())
