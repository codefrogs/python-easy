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
    task = asyncio.create_task(do_calc('+'), name="task-one")

    # we make sure we keep a record of the task to prevent
    # garbage collection.
    tasks.add(task)

    # We get the task to remove itself when finished
    task.add_done_callback(tasks.discard)
    result = await task
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
