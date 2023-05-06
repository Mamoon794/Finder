import os
import signal

path  = "/Users"
count = 0

def signal_handler(signal, frame):
    print(path)
    print(count)


class Node:
    def __init__(self, data):
        self.value = data
        self.prev = None
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def add(self, node):
        if self.is_empty():
            self.head = node
        else:
            self.tail.next = node
            node.prev = self.tail
        self.tail = node

    def poping(self):
        node = self.tail
        if self.tail == self.head:
            self.head = None
            self.tail = None
        else:
            self.tail = node.prev
            self.tail.next = None
        return node.value


