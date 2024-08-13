README.txt

Previously we had a CPU problem. We can solve that by using 'selectors'.
First take a look at 'select_ex', then come back here and trial out the server.

Now start up server_sequencial.
Connect one or more clients.

But we are being slightly crafty. We've set our LISTEN_TIMEOUT to '1'. If we did set it to 0 then
the CPU will max out once more.

However, in principle, what we are doing here is not far off what asyncio does.

