#!/usr/bin/env python3

from multiprocessing import Pool

def main():
  with Pool(1) as pool:
    print("Pool created")

  print("Closed & Terminated.")

# This is the safest way to create a pool.

if __name__ == "__main__":
    main()

