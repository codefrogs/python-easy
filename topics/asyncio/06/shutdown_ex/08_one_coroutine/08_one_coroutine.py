#!/usr/bin/env python3
import asyncio
import logging
import signal

async def main():

    setup_event_loop()

    # Some blocking action
    print("Blocking activity started (20s)!...")
    print("Press CTRL-C to raise an interrupt.")

    try:

        await asyncio.sleep(20)

    except asyncio.CancelledError:  
        print('Sleep Cancelled!')
        #logging.exception(e)
    
    finally:
        print("Cleaning up...")
        pass

    print("*** Finished ***")

def setup_event_loop():
    event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    event_loop.add_signal_handler(signal.SIGINT, handle_interrupt)

def handle_interrupt():
    tasks = asyncio.all_tasks()
    for task in tasks:
        print(f"\nCancelling task({task.get_name()})")
        task.cancel()  # This should raise an exception in the task.

if __name__ == "__main__":
    asyncio.run(main())
