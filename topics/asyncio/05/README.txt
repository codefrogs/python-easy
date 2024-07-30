README.txt

This is our first step into asyncio. We've added an async coroutine to process
the network connections, a task for the prime calculator, and a task to manage
a client connection.

We are going to use the asyncio 'event loop', and reference it directly.

We should note that the documentation says:

"Application developers should typically use the high-level asyncio functions,
such as asyncio.run(), and should rarely need to reference the loop object
or call its methods."

But we are just exploring and evolving our server here, and this should help
our understanding.

But we see two problems:

1. The CPU task holds up the event loop. It isn't a good
fit as it doesn't have any IO-bound calls.

2. Shutdown is not well handled if there are any exceptions.

see also: https://docs.python.org/3/library/asyncio-task.html#task-cancellation
