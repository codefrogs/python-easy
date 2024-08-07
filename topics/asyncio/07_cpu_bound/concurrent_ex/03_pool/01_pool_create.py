#!/usr/bin/env python3

from multiprocessing import Pool

def main():
    pool = Pool(1)
    print("Pool created")
    pool.close()
    print("Pool closed")
    pool.terminate()
    print("Pool terminated")

# This is how we can create a pool, but it's better 
# with using a context manager.

if __name__ == "__main__":
    main()

