class PrimeCalculator:

    def __init__(self):
        self.current_prime = 3

    def find_next(self):
        num = self.current_prime
        found = False

        while (not found):
            num = num + 2
            if self.is_prime(num):
                found = True
                self.current_prime = num

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
