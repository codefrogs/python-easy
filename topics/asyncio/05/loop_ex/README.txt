README.txt

We will use sockets with asyncio.

But note the following from the documentation:

"In general, protocol implementations that use transport-based APIs such as
 loop.create_connection() and loop.create_server() are faster than
 implementations that work with sockets directly.
 However, there are some use cases when performance is not critical,
 and working with socket objects directly is more convenient."

 But we are just exploring how to use asyncio and add it to our previous example.

 see: https://docs.python.org/3.10/library/asyncio-eventloop.html#working-with-socket-objects-directly
