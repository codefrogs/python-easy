#!/usr/bin/env python3

# Based on the quickstart page: https://docs.aiohttp.org/en/stable/client_quickstart.html

import aiohttp # This is the async client/server framework
import asyncio # python asyncio library

async def main():
    # We want just a client session.
    # Typically you use just one client session for an application.
    #
    # Notice we are using 'async with' here.
    #
    async with aiohttp.ClientSession() as session:

      # Now we have a session, so we can send a 'get' request.
      async with session.get("http://httpbin.org/get") as resp:

        # Now we have a response.
        # We get the status.
        print(resp.status)
    
    print("Finished")

if __name__ == "__main__":
    asyncio.run(main())
