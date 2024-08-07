#!/usr/bin/env python3
import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import Any
import time

def cpu_func() -> None:    
    for _ in range(10):
        time.sleep(1)    
        print(".")

async def task_io() -> None:    
    for _ in range(10):
        await asyncio.sleep(1)  # Simulate an I/O operation with a 2-second delay
        print("+")

async def task_cpu(executor: ProcessPoolExecutor) -> Any:    
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, cpu_func)    

async def main() -> None:
        
    with ProcessPoolExecutor() as pool:        
        io_task = asyncio.create_task(task_io())        
        cpu_task = asyncio.create_task(task_cpu(pool))
        
        # Await both tasks
        await asyncio.gather(io_task, cpu_task)

if __name__ == '__main__':
    asyncio.run(main())
