README.txt

This is our first step into asyncio. We've added an async coroutine to process
the network connections.
Using asyncio.create_taskasyncio.create_task(), we have added a task for the prime
calculator, and a task to manage client connections.

We use the asyncio 'event loop' directly.

Note however that the documentation says:

"Application developers should typically use the high-level asyncio functions,
such as asyncio.run(), and should rarely need to reference the loop object
or call its methods."

But we are just exploring and evolving our server here, and this should help
our understanding.

But there are a few problems with our solution:

1. The CPU task holds up the event loop. It is not a good
   fit, as it does not make any IO-bound calls.

2. Shutdown is not well handled if there are any exceptions.
   So, when we try to cancel the server with CTRL-C it does
   not shutdown gracefully.

3. If any of the socket operations raise an exception, they
   are not handled.

see also: https://docs.python.org/3/library/asyncio-task.html#task-cancellation
