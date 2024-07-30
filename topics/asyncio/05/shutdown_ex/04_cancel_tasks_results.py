#!/usr/bin/env python3
import asyncio

tasks = set()

# This is some long running calculation.
async def do_calc(symbol) -> int:
    i = 0
    while i < 20:
        i += 1
        print_symbol(symbol)
        await asyncio.sleep(1)

    print()
    return i

def print_symbol(symbol):
    print(symbol, end="", flush=True) # Return the result

async def main():

    # We create a task for 'do_calc'
    task1 = asyncio.create_task(do_calc('+'), name="task-one")
    task2 = asyncio.create_task(do_calc('*'), name="task-two")

    # we make sure we keep a record of the task to prevent
    # garbage collection.
    tasks.add(task1)
    tasks.add(task2)

    # We get the task to remove itself when finished
    task1.add_done_callback(tasks.discard)
    task2.add_done_callback(tasks.discard)

    # We give the two tasks a moment to run
    await asyncio.sleep(3)

    # Let's cancel all the tasks
    for task in tasks:
        task.cancel()

    print()
    print("Tasks cancelled.")    

    result = await task1
    print(f"Result(+): {result}\n") #  We never get here!
    
    result = await task2            #  We never get here!
    print(f"Result(*): {result}\n") #  We never get here!

    await do_calc("@")              #  We never get here!
    print("*** Finished ***")       #  We never get here!

if __name__ == "__main__":
    asyncio.run(main())
