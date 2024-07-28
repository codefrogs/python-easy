#!/usr/bin/env python3

# In this example, we explore the data types related to 'selectors'.
# This server waits 60s for a client to connect, and then
# shows the related IO notification gathered.

import socket
import selectors

# Below are the key types we want to be aware of.
# Central to these is the 'SelectorKey'. As the documentation states, it connects the 'file object'
# to its underlying 'file descriptor'. Remember that on Linux, everything is a file, and that includes sockets.
#
# See also: https://docs.python.org/3.10/library/selectors.html?highlight=selectorkey#selectors.SelectorKey

SelectorEvents = int  # e.g. EVENT_READ, EVENT_WRITE
FileObjectInfo = tuple[selectors.SelectorKey, SelectorEvents]
FileObjectInfoList = list[FileObjectInfo]

class ServerSelect:
            
    LISTEN_TIMEOUT = 60 

    def __init__(self):
        self.HOST = ''     # Symbolic name meaning all available interfaces
        self.PORT = 50007  # Arbitrary non-privileged port
        self.socket = None
        self.event_monitor = selectors.DefaultSelector()

    def run(self):
        self.create_socket()
        self.setup_socket()
        self.setup_event_monitor()
        
        print("Listening (15s)...")
        sel_event_list: FileObjectInfoList = self.event_monitor.select(timeout=self.LISTEN_TIMEOUT) # blocking
        
        for selector_key, events in sel_event_list:
            
            self.show_selector_key(selector_key)
            self.show_events(events)

        self.close_socket()

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def setup_socket(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST, self.PORT))    
        self.socket.setblocking(False)
        self.socket.listen()

    def setup_event_monitor(self):
        self.event_monitor.register(self.socket, selectors.EVENT_READ)
       
    def show_selector_key(self, key: selectors.SelectorKey):
        obj_text = self.fileobj_to_str(key.fileobj)
        print(f"SelectorKey:\n"
              f"    fileobj: {obj_text}\n"
              f"    fd:      {key.fd}\n"
              f"    events:  {self.event_to_str(key.events)}\n"
              f"    data:    {key.data}")
        
    def fileobj_to_str(self, fileobj):
        return (f"family: {fileobj.family}, type: {fileobj.type}, proto: {fileobj.proto} addrs: {fileobj.getsockname()}")        

    def show_events(self, event: SelectorEvents):
        print("Events: ", self.event_to_str(event))

    def event_to_str(self, event: SelectorEvents):
        bits = []
        event_map = { selectors.EVENT_READ:  "EVENT_READ", 
                      selectors.EVENT_WRITE: "EVENT_WRITE" }

        for key, name in event_map.items():
            if (key & event):
                bits.append(name)

        return '|'.join(bits)        

    def close_socket(self):
        self.socket.close()


def main():
    server = ServerSelect()
    server.run()
    print("Server finished.")

if __name__ == "__main__":
    main()
