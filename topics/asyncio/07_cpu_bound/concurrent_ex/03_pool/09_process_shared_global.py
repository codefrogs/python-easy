#!/usr/bin/env python3

from multiprocessing import Process
from multiprocessing import Value
from concurrent.futures import ProcessPoolExecutor
from typing import Optional

sum: Optional[Value] = None

# This may look simple, but also slightly odd perhaps.
# This is called by the pool for each process.
# This function is called in each process.
# It first declares that 'sum' is global, and not local to the function.
# We then pass it a reference to the 'shared memory' value from the main
# process.
# Now the child process has a reference to the 'cnt' variable from the main process.
# So each process will not operate on the *same* sum value.
def init(shared: Value):
    global sum
    sum = shared

def count(max: int) -> int:
    global sum
    with sum.get_lock():
        for i in range(max):
            sum.value += 1               
    # return sum # You can't do this as 'Value' is not serialisable.

def main():
    COUNT_MAX=20

    # We have to declare this to be global (no local)
    global sum 
    sum = Value('i', 0) # We declare an integer with value zero.
    
    with ProcessPoolExecutor(initializer=init, initargs=(sum,)) as pool:
      future_object = pool.submit(count, COUNT_MAX) # One process      
      future_object.result() # blocks until we get the result.

    print(f"Total: {sum.value}")

    # So we have now a global variable, and a process, but how do we now add
    # asyncio to this?
    # We want to use the event loop to do some I/O function and run the
    # count function.
    
if __name__ == "__main__":
    main()
