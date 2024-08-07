#!/usr/bin/env python3

from multiprocessing import Process

def hello():
    print("Hello world!")

def main():
    p = Process(target=hello)
    
    # Nothing happens yet, we need to start the process
    p.start()
    p.join()

# This is required!
if __name__ == "__main__":
    main()
