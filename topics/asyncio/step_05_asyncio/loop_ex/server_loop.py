#!/usr/bin/env python3

# In this example, we explore the use of the asyncio event loop.
# We no longer use 'selectors' here.

import socket
import asyncio


class ServerLoop:

    def __init__(self):
        self.HOST = ''     # Symbolic name meaning all available interfaces
        self.PORT = 50007  # Arbitrary non-privileged port
        self.server_socket = None
        self.current_client: socket.socket = None
        self.event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    async def run(self):
        self.create_server_socket()
        self.setup_server_socket()

        await self.run_networking()

        print("Shutting down...")

        self.close_client_socket()
        self.close_server_socket()

    def create_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close_client_socket(self):
        self.current_client.close()

    def setup_server_socket(self):
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.setblocking(False)
        self.server_socket.listen()

    async def run_networking(self):
        print("Listening ...")
        self.current_client, addr = await self.event_loop.sock_accept(self.server_socket)
        self.current_client.setblocking(False)
        print("Client connected at: ", addr)

    def close_server_socket(self):
        self.server_socket.close()


async def main():
    server = ServerLoop()
    await server.run()
    print("Server finished.")

if __name__ == "__main__":
    asyncio.run(main())
