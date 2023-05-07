import os
import signal
import sys

# path  = "/Users/primus/Documents"
count = 0
ass = 0

def signal_handler(signal, frame):
    # print(path)
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

w = open("output.txt", 'w')
w.close()

ws = open("result.txt", "w")

def list_find(thePath, c, shouldFork=False):

    theCount = c
    amount = 0
    lst = LinkedList()
    node1 = Node(thePath)
    lst.add(node1)
    prev = ""
    while lst.head and lst.tail:
        try:
            paths = lst.poping()
            if prev == paths:

                # print(path)
                pass
            else:
                prev = paths

            obj = os.scandir(paths)
            for entry in obj:
                if entry.is_file():
                    if "/Users/primus/.DS_Store" in  str(entry.path):
                        print("here")
                    ws.write(entry.path)
                    ws.write("\n")
                    theCount += 1


                elif entry.is_dir() and not os.path.islink(entry.path):
                    if amount < 4 and shouldFork:
                        amount += 1
                        pid = os.fork()


                        if pid == 0:
                            lst = None
                            obj.close()
                            files = list_find(entry.path, 0, False)
                            w = open("output.txt", 'a')
                            w.write(str(files))
                            w.write("\n")
                            w.close()
                            exit(0)


                    else:
                        try:
                            childPid, _ = os.waitpid(-1, os.WNOHANG)
                            if childPid != 0:
                                amount -= 1
                        except ChildProcessError:
                            pass
                        node1 = Node(entry.path)
                        lst.add(node1)
            obj.close()

        except PermissionError as e:
            pass

    if shouldFork:
        pid = 2
        try:
            while pid > 0:
                pid, status = os.wait()
        except ChildProcessError:

            r = open("output.txt", "r")
            message = r.readline()
            while message:
                theCount += int(message)
                message = r.readline()

            r.close()

    return theCount



signal.signal(signal.SIGINT, signal_handler)
c = list_find('/Users/primus', count, True)
#
ws.close()
print(c)
