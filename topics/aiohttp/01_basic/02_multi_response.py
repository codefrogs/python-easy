#!/usr/bin/env python3

# Based on the quickstart page: https://docs.aiohttp.org/en/stable/client_quickstart.html

import aiohttp  # This is the async client/server framework
import asyncio  # python asyncio library

base_url = "http://www.example.com/"
urls = [ base_url + url for url in ['', 'some', 'links', "and", "more"]]

async def fetch_resp(session, url):

    async with session.get(url) as resp:
        val= resp.status

    return val

async def main():
    # We want one client session.
    async with aiohttp.ClientSession() as session:

        # We want to concurrently do a get for each URL.
        tasks = [fetch_resp(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    # Now we have a response.
    # We get the status.
    for result in results:
        print(result)

    print("Finished")

if __name__ == "__main__":
    print(urls)
    asyncio.run(main())
