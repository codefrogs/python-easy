#!/usr/bin/env python3
# Echo client program
import socket
import time


class PrimeClient:
    """Prime client"""

    def __init__(self):
        self.socket = None
        self.HOST = 'localhost'    # The remote host
        self.PORT = 50007          # The same port as used by the server

    def run(self):
        self.setup_socket()
        self.connect_to_server()        

        self.get_primes()

        self.clean_up()

    def setup_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       

    def connect_to_server(self):
        self.socket.connect((self.HOST, self.PORT))
        print("Connected")

    def get_primes(self):
        for i in range(4):
            prime = self.get_prime()
            print(prime)
            time.sleep(1)

    def get_prime(self):
        self.socket.sendall(b'get')
        data: bytes = self.socket.recv(4)  # Get value
        value: int = int.from_bytes(data, 'big')
        return value 

    def clean_up(self):
        self.shutdown_server()
        self.close_socket()

    def shutdown_server(self):
        self.socket.sendall(b'end')

    def close_socket(self):
        self.socket.close()

def main():
    
    prime_client = PrimeClient()
    prime_client.run()

if __name__ == "__main__":
    main()
