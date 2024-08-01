README.txt

With the knowledge gained in the shudown_ex folder we have updated this
script to cancel all the tasks and catch the CancelError exceptions.

This still isn't production quality however.

For example:

1. What do we do if, while we are cancelling all the tasks, a new client connects?
2. How do we arrange for the CPU bound task to run without blocking the event loop?

