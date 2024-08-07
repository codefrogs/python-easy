#!/usr/bin/env python3
import asyncio
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Value
from typing import Optional, Any
import time

sum: Optional[Value] = None

def init(shared: Value):
    global sum
    sum = shared

def cpu_func(max: int) -> int:
    global sum
    
    for i in range(max):
        with sum.get_lock():
            sum.value += 1
        time.sleep(1)
        print(f".")

async def task_io(delay: int):
    for _ in range(20):
        await asyncio.sleep(delay)
        print("+")

async def task_reporter(delay: int):
    global sum
    for _ in range(20):
        await asyncio.sleep(delay)
        print("Reporter: Sum= ", sum.value, flush=True)

async def task_cpu(pool):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(pool, cpu_func, 20)

async def main():
    # Create the pool
    COUNT_MAX=20
    global sum 
    sum = Value('i', 0) # We declare an integer with value zero.
        
    io_task = asyncio.create_task(task_io(1))
    reporter_task = asyncio.create_task(task_reporter(1))

    with ProcessPoolExecutor(initializer=init, initargs=(sum,)) as pool:      
        cpu_task = asyncio.create_task(task_cpu(pool))

        await asyncio.gather(io_task, reporter_task, cpu_task)
    
# This does what we wanted. We now have the IO bound tasks and CPU bound tasks
# working with the event loop!

if __name__ == "__main__":
   asyncio.run(main())
