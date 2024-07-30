#!/usr/bin/env python3

# Async prime server example:
# Initial attempt at adding asyncio.
#
import socket
import asyncio
from prime_calculator import PrimeCalculator
from enum import Enum, auto


class ServerEvent(Enum):
    INITIALISED_EVT = auto()
    SHUTDOWN_EVT = auto()


class Command(Enum):
    SHUTDOWN_CMD = auto()
    GET_PRIME_CMD = auto()
    UNKNOWN_CMD = auto()


class ServerState(Enum):
    NULL_STATE = auto()
    RUNNING_STATE = auto()
    SHUTDOWN_STATE = auto()


class PrimeServerAsync:
    """Primer number server using async"""

    LISTEN_TIMEOUT = 1  # If we use '0' here, we'll be maxing out the CPU again!
    BUFFER_LEN = 1024
    PORT_NUM_INDEX = 1
    SELECT_TIMEOUT = 0  # => Non-blocking

    def __init__(self):
        self.HOST = ''     # Symbolic name meaning all available interfaces
        self.PORT = 50007  # Arbitrary non-privileged port
        self.server_socket: socket.socket = None
        self.current_client: socket.socket = None
        self.state = ServerState.NULL_STATE
        self.prime_calculator = PrimeCalculator()
        self.event_loop: asyncio.AbstractEventLoop = None

    async def run(self):
        self.init()

        # Nice try! But wrong approach for CPU-bound work!
        asyncio.create_task(self.run_prime_search())

        while (self.state != ServerState.SHUTDOWN_STATE):
            await self.run_networking()

        print("Shutting down...")

    def init(self):
        print("init...", end="")
        self.create_server_socket()
        self.setup_server_socket()
        self.setup_event_loop()
        self.update_state(ServerEvent.INITIALISED_EVT)
        print("Done")

    def create_server_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setup_server_socket(self):
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.setblocking(False)
        self.server_socket.listen()

    def setup_event_loop(self):
        self.event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    def update_state(self, event: ServerEvent):

        if (event == ServerEvent.INITIALISED_EVT):
            self.state = ServerState.RUNNING_STATE

        elif (event == ServerEvent.SHUTDOWN_EVT):
            self.state = ServerState.SHUTDOWN_STATE

    # This coroutine would hold up everthing in the event loop without
    # the sleep().
    async def run_prime_search(self):
        while (self.state != ServerState.SHUTDOWN_STATE):
            await asyncio.sleep(1)
            self.prime_calculator.find_next()

    async def run_networking(self):
        print("Listening ...")

        while (self.state != ServerState.SHUTDOWN_STATE):
            connection, addr = await self.event_loop.sock_accept(self.server_socket)
            self.process_new_client(connection)

            print("Client new: ", addr)

    def process_new_client(self, connection):
        self.add_new_client(connection)
        asyncio.create_task(self.process_client(connection))

    def add_new_client(self, connection):
        connection.setblocking(False)

    async def process_client(self, connection):
        is_ok = True
        while is_ok:
            data = await self.get_client_data(connection)
            is_ok = await self.process_client_data(connection, data)

        connection.close()

    async def get_client_data(self, connection):
        return await self.event_loop.sock_recv(connection, self.BUFFER_LEN)

    def get_port_number(self, connection):
        return connection.getpeername()[self.PORT_NUM_INDEX]

    async def process_client_data(self, connection, data):
        if not data:
            self.remove_client(connection)
            return False  # => Lost the client
        else:
            await self.process_data(connection, data)

        return True

    def remove_client(self, connection):
        client_port = self.get_port_number(connection)
        print(f"Client lost({client_port})")
        connection.close()

    async def process_data(self, connection, data):
        cmd = self.get_command(data)
        await self.process_command(connection, cmd)

    def get_command(self, msg):
        if (msg == b'end'):
            cmd = Command.SHUTDOWN_CMD
        elif (msg == b'get'):
            cmd = Command.GET_PRIME_CMD
        else:
            cmd = Command.UNKNOWN_CMD
        return cmd

    async def process_command(self, connection, cmd):
        if (cmd == Command.SHUTDOWN_CMD):
            self.shutdown()

        elif (cmd == Command.GET_PRIME_CMD):
            await self.send_client_prime(connection)

        elif (cmd == Command.UNKNOWN_CMD):
            print("Client sent unknown command!")
        else:
            print("Command type not recognised!")

    def shutdown(self):
        self.close_server_socket()
        self.update_state(ServerEvent.SHUTDOWN_EVT)

    def close_server_socket(self):
        self.server_socket.close()

    async def send_client_prime(self, connection):
        val = self.prime_calculator.get_latest()
        await self.send_val_to_client(connection, val)

    async def send_val_to_client(self, connection, val):
        data = val.to_bytes(4, byteorder='big')
        await self.event_loop.sock_sendall(connection, data)


async def main():
    server = PrimeServerAsync()
    await server.run()
    print("Server finished.")

if __name__ == "__main__":
    asyncio.run(main())
