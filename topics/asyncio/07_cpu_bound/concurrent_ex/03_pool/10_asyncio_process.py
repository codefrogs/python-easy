#!/usr/bin/env python3

from multiprocessing import Process
from multiprocessing import Value
from concurrent.futures import ProcessPoolExecutor
from typing import Optional
import asyncio
import time

sum: Optional[Value] = None

# This may look simple, but also slightly odd perhaps.
# This is called by the pool for each process.
# It first declares that 'sum' is global, and not local to the function.
# We then pass it a reference to the 'shared memory' value from the main
# process.
# Now the child process has a reference to the global variable from the main process.
# Each process will now operate on the *same* sum value.
def init(shared: Value):
    global sum
    sum = shared

def count(max: int) -> int:
    global sum
    
    for i in range(max):
        with sum.get_lock():
            sum.value += 1
        time.sleep(1)
        print(".", end='')

async def task_io(delay: int):
    for _ in range(5):
        await asyncio.sleep(delay)
        print("Running IO-task")

async def task_reporter(delay: int):
    for _ in range(5):
        await asyncio.sleep(delay)
        print("Sum: ", sum.value)

async def main():
    
    # Create two asyncio tasks
    task1 = asyncio.create_task(task_io(1), name="task_io")
    task2 = asyncio.create_task(task_reporter(1), name="task_reporter")

    # Create the pool
    COUNT_MAX=5
    global sum 
    sum = Value('i', 0) # We declare an integer with value zero.

    with ProcessPoolExecutor(initializer=init, initargs=(sum,)) as pool:
      future_object = pool.submit(count, COUNT_MAX) # One process      
      future_object.result() # blocks until we get the result.
    
    print("Finished CPU bound.")

    await task1
    await task2

    # A good first try...but this doesn't exactly do what we want.
    # It does create two tasks, and start them on the event loop...
    # It runs the process, and then continues with the tasks! 
    # It seems to hold up the event loop waiting on 'future_object'!
    
if __name__ == "__main__":
   asyncio.run(main())
