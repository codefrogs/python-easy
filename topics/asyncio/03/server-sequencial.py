#!/usr/bin/env python3

# Sequencial prime server example:
# Attempt to handle multiple client connections.
#

import socket
from prime_calculator import PrimeCalculator
from enum import Enum, auto

class ServerEvent(Enum):
    INITIALISED_EVT = auto()
    LOST_CLIENT_EVT = auto()    
    SHUTDOWN_EVT    = auto()

class Command(Enum):
    NULL_CMD      = auto()
    SHUTDOWN_CMD  = auto()
    GET_PRIME_CMD = auto()
    UNKNOWN_CMD   = auto()

class ServerState(Enum):
    NULL_STATE             = auto()
    LISTENING_STATE        = auto()    
    SHUTDOWN_STATE         = auto()

class PrimeServer:
    """Prime number server"""

    BUFFER_LEN = 1024
    PORT_NUM_INDEX = 1

    def __init__(self):
        self.HOST = ''     # Symbolic name meaning all available interfaces
        self.PORT = 50007  # Arbitrary non-privileged port
        self.socket = None
        self.current_client = None
        self.connections = [] # Holds the connections
        self.state = ServerState.NULL_STATE
        self.prime_calculator = PrimeCalculator()        

    def run(self):

        while (self.state != ServerState.SHUTDOWN_STATE):            
            self.run_processes()
            print()

    def run_processes(self):        
        self.run_prime_search()
        self.run_next_process()        

    def run_prime_search(self):
        print("Finding next prime..", end="")
        self.prime_calculator.find_next()
        #print("Done.")
        
    def run_next_process(self):        
        if (self.state == ServerState.NULL_STATE):
            self.init()

        elif (self.state == ServerState.LISTENING_STATE):
            self.listen_for_connection()        
            self.serve_clients()

        elif (self.state == ServerState.SHUTDOWN_STATE):
            print("Shutting down...")
            pass  # No longer processing anything!

        else:
            print("Unknown state!", self.state)        

    def init(self):
        print("init...", end="")
        self.create_socket()
        self.setup_socket()
        self.update_state(ServerEvent.INITIALISED_EVT)
        print("Done")

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setup_socket(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST, self.PORT))    
        self.socket.setblocking(False)    

    def update_state(self, event: ServerEvent):

        if (event == ServerEvent.INITIALISED_EVT):
            self.state = ServerState.LISTENING_STATE

        elif (event == ServerEvent.SHUTDOWN_EVT):
            self.state = ServerState.SHUTDOWN_STATE

    def listen_for_connection(self):
        print("Listening (blocking)..", end="", flush=True)
        
        try:
            # Enable listening
            self.socket.listen(1)
            
            connection, addr = self.socket.accept() # blocks
            connection.setblocking(False)
            self.connections.append(connection)            
            
            self.show_connection(addr)

        except BlockingIOError:
            # We just ignore these failures!
            pass
        #print("Done.")

    def show_connection(self, addr):
        print('Connected by', addr)

    def serve_clients(self):
        for connection in self.connections:            
            self.serve_client(connection)

    def serve_client(self, connection): 
        index = connection.getpeername()[self.PORT_NUM_INDEX]
        print(f"Serving client({index}).", end="")
        try:
            self.current_client = connection

            data = self.get_data()
            if not data:
                print("No data")
                self.remove_client()
            else:
                self.process_data(data)

        except BlockingIOError:
            # Just ignore failure to read
            pass

        #print("Done")

    def get_data(self):
        return self.current_client.recv(self.BUFFER_LEN)

    def remove_client(self):
        print(f"Client lost: {self.current_client}")      
        self.current_client.close()
        self.connections.remove(self.current_client)

    def process_data(self, data):
        cmd = self.get_command(data)
        self.process_command(cmd)

    def get_command(self, msg):
        if (msg == b'end'):
            cmd = Command.SHUTDOWN_CMD
        elif (msg == b'get'):
            cmd = Command.GET_PRIME_CMD
        else:
            cmd = Command.UNKNOWN_CMD
        return cmd

    def process_command(self, cmd):
        if (cmd == Command.SHUTDOWN_CMD):            
            self.shutdown()

        elif (cmd == Command.GET_PRIME_CMD):
            self.send_client_prime()

        elif (cmd == Command.UNKNOWN_CMD):
            print("Client sent unknown command!")
        else:
            print("Command type not recognised!")

    def shutdown(self):
        self.connections.close()
        self.close_socket()
        self.update_state(ServerEvent.SHUTDOWN_EVT)

    def close_socket(self):
        self.socket.close()

    def send_client_prime(self):
        val = self.prime_calculator.get_latest()
        self.send_val_to_client(val)

    def send_val_to_client(self, val):
        self.current_client.sendall(val.to_bytes(4, byteorder='big'))

def main():
    server = PrimeServer()
    server.run()
    print("Server finished.")

if __name__ == "__main__":
    main()
