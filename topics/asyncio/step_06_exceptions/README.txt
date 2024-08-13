README.txt
Go through shutdown_ex examples first. Then come back here.

With the knowledge gained in the shudown_ex folder we have updated this
script to cancel all the tasks and catch the CancelError exceptions.

Start up the server.
Then do a CTRL-C on the server. It should now shut down gracefully.

This still isn't production quality however.

For example:

1. It issues an exception on CTRL-C when a client is connected.
2. What do we do if, while we are cancelling all the tasks, a new client connects?
3. How do we arrange for the CPU bound task to run without blocking the event loop?

