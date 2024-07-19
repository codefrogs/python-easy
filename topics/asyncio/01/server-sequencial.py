#!/usr/bin/env python3

# Prime server
# (Based on the 'Echo server')
#

import socket
from prime_calculator import PrimeCalculator
from enum import Enum, auto

class ServerEvent(Enum):    
    INITIALISED_EVT = auto()
    LOST_CLIENT_EVT = auto()
    NEW_CLIENT_EVT  = auto()     
    SHUTDOWN_EVT    = auto()    

class Command(Enum):
    NULL_CMD      = auto()
    SHUTDOWN_CMD  = auto()    
    GET_PRIME_CMD = auto()
    UNKNOWN_CMD   = auto()

class ServerState(Enum):
    NULL_STATE             = auto()
    LISTENING_STATE        = auto()
    CLIENT_CONNECTED_STATE = auto()    
    SHUTDOWN_STATE         = auto()    

class PrimeServer:
    """Primer number server"""

    BUFFER_LEN = 1024

    def __init__(self):
        self.HOST = ''     # Symbolic name meaning all available interfaces
        self.PORT = 50007  # Arbitrary non-privileged port
        self.socket = None
        self.conn = None
        self.state = ServerState.NULL_STATE
        self.event_queue = []
        self.prime_calculator = PrimeCalculator()
    
    def run(self):
        
        while( self.state != ServerState.SHUTDOWN_STATE):            
            self.run_process()

    def run_process(self):
        self.calculate_next_prime()
        self.run_state_process()

    def run_state_process(self):
        if (self.state == ServerState.NULL_STATE):
            self.init()

        elif (self.state == ServerState.LISTENING_STATE):
            self.listen_for_connection()
            
        elif (self.state == ServerState.CLIENT_CONNECTED_STATE):
            self.serve_client()            

        elif (self.state == ServerState.SHUTDOWN_STATE):
            pass # No longer processing anything!

        else:
            print("Unknown state!", self.state)

    def calculate_next_prime(self):
        self.prime_calculator.find_next()

    def init(self):
        self.create_socket()
        self.setup_socket()
        self.update_state(ServerEvent.INITIALISED_EVT)

    def update_state(self, event: ServerEvent):
     
        if (event == ServerEvent.INITIALISED_EVT):
            self.state = ServerState.LISTENING_STATE

        elif ( event == ServerEvent.NEW_CLIENT_EVT):
            self.state = ServerState.CLIENT_CONNECTED_STATE

        elif (event == ServerEvent.LOST_CLIENT_EVT):
            self.state = ServerState.LISTENING_STATE

        elif (event == ServerEvent.SHUTDOWN_EVT):
            self.state = ServerState.SHUTDOWN_STATE        

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setup_socket(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST, self.PORT))        

    def listen_for_connection(self):        
        self.socket.listen(1)
        self.conn, addr = self.socket.accept()
        self.show_connection(addr)
        self.update_state(ServerEvent.NEW_CLIENT_EVT)        

    def shutdown(self):
        self.conn.close()
        self.close_socket()
        self.update_state(ServerEvent.SHUTDOWN_EVT)

    def close_socket(self):
        self.socket.close()

    def show_connection(self, addr):
        print('Connected by', addr)

    def serve_client(self):        
        data = self.get_data()
        if not data:
            print("No data")
            self.update_state(ServerEvent.LOST_CLIENT_EVT)
        else:
            self.process_data(data) 

    def get_data(self):
        return self.conn.recv(self.BUFFER_LEN)

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

    def send_client_prime(self):
        val = self.prime_calculator.get_latest()
        self.send_val_to_client(val)

    def send_val_to_client(self, val):        
        self.conn.sendall(val.to_bytes(4, byteorder='big'))

    def get_next_prime(self):
        return 11

def main():
    server = PrimeServer()
    server.run()
    print("Server finished.")

if __name__ == "__main__":
    main()