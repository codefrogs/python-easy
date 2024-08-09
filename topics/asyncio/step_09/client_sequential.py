#!/usr/bin/env python3
# Echo client program
import socket
import time


class PrimeClient:
    """Prime client"""

    SLEEP_DELAY = 3  # Delay between each request.
    PRIMES_NUM = 10  # Number of primes to get.

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
        print("Connected!")

    def get_primes(self):
        for i in range(self.PRIMES_NUM):
            prime = self.get_prime()
            time.sleep(self.SLEEP_DELAY)
            print(prime)

    def get_prime(self):
        self.socket.sendall(b'get')
        data: bytes = self.socket.recv(4)  # Get value
        value: int = int.from_bytes(data, 'big')
        return value

    def clean_up(self):
        self.close_socket()

    def close_socket(self):
        self.socket.close()


def main():

    prime_client = PrimeClient()
    prime_client.run()


if __name__ == "__main__":
    main()
