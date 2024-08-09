from step_09 import globals
import time


class PrimeCalculator:

    def __init__(self):
        self.current_prime = 3

    def run(self):
        print("Searching primes...")

        while (globals.running.value == 1):
            time.sleep(1)
            self.set_next_prime()

        print("Searching primes: STOPPED.", flush=True)

    def find_next(self):
        num = self.current_prime
        found = False

        while (not found):
            num = num + 2
            if self.is_prime(num):
                found = True
                self.current_prime = num

        self.update_global()

    def is_prime(self, num):
        found_prime = True
        max_divisor = int(num ** 0.5) + 1
        for i in range(3, max_divisor):
            if (num % i == 0):
                found_prime = False
                break
        return found_prime

    def get_latest(self):
        return self.current_prime

    def update_global(self):
        with globals.prime.get_lock():
            globals.prime.value = self.get_latest()

    def set_next_prime(self):
        self.find_next()
