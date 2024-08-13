#!/usr/bin/env python3
import asyncio
import logging
import signal

tasks = set()


async def main():

    setup_event_loop()

    # We create a task for 'do_calc'
    task1 = asyncio.create_task(do_calc('+'), name="task-one")
    task2 = asyncio.create_task(do_calc('*'), name="task-two")

    # we make sure we keep a record of the task to prevent
    # garbage collection.
    tasks.add(task1)
    tasks.add(task2)

    # We get the task to remove itself from 'tasks' when finished
    task1.add_done_callback(tasks.discard)
    task2.add_done_callback(tasks.discard)

    result = await task1
    print(f"Result(+): {result}")

    result = await task2
    print(f"Result(*): {result}")

    print("*** Finished ***")


def setup_event_loop():
    event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    event_loop.add_signal_handler(signal.SIGINT, handle_interrupt)


def handle_interrupt():
    tasks = asyncio.all_tasks()
    for task in tasks:
        print(f"Cancelling task({task.get_name()})")
        task.cancel()  # This should raise an exception in the task.

# This is some long running calculation.


async def do_calc(symbol) -> int:
    try:
        i = 0
        while i < 20:
            i += 1
            print_symbol(symbol)
            await asyncio.sleep(1)

        print()
    except Exception as e:
        task_name = asyncio.current_task().get_name()
        print(f"Caught exception ({task_name}): ", e)
        logging.exception(e)

    finally:
        task_name = asyncio.current_task().get_name()
        print(f"Cleaning up task ({task_name})")
        return i


def print_symbol(symbol):
    print(symbol, end="", flush=True)  # Return the result


if __name__ == "__main__":
    asyncio.run(main())
