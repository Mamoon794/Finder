import os
import signal
import sys
import time

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
        self.size = 0

    def is_empty(self):
        return self.head is None

    def add(self, node):
        if self.is_empty():
            self.head = node
        else:
            self.tail.next = node
            node.prev = self.tail
        self.tail = node
        self.size += 1

    def poping(self):
        self.size -= 1
        node = self.tail
        if self.tail == self.head:
            self.head = None
            self.tail = None
        else:
            self.tail = node.prev
            self.tail.next = None
        return node.value




def list_find2(thePath, theCount, writing):
    try:
        obj = os.scandir(thePath)
        for entry in obj:
            if entry.is_file() and not entry.is_symlink():
                theCount += 1

            if entry.is_dir() and not os.path.islink(entry.path):

                writing.write(entry.path)


    except PermissionError:
        pass
    return theCount


def readMessage(codes):
    os.close(codes[0])
    r = os.fdopen(codes[1])
    message = r.read()
    r.close()
    return int(message)


def list_find(thePath, c):

    theCount = c
    amount = 0
    lst = LinkedList()
    node1 = Node(thePath)
    lst.add(node1)
    prev = ""

    pipeCodes = dict()
    while lst.head and lst.tail:
        try:
            paths = lst.poping()
            if prev == paths:

                print(paths)
            else:
                prev = paths

            obj = os.scandir(paths)
            for entry in obj:
                if entry.is_file() and not entry.is_symlink():
                    theCount += 1


                elif entry.is_dir() and not os.path.islink(entry.path):
                    if amount < 40:
                        amount += 1
                        rea, wri = os.pipe()
                        pid = os.fork()


                        if pid == 0:
                            lst = None
                            obj.close()
                            wri = os.fdopen(wri, 'w')
                            files = list_find2(entry.path, 0, wri)
                            wri.write("now for the amount:")
                            wri.write(str(files))
                            wri.close()
                            os.kill(os.getpid(), signal.SIGKILL)

                        else:
                            pipeCodes[pid] = [wri, rea]


                    else:
                        try:
                            childPid, _ = os.waitpid(-1, os.WNOHANG)
                            while childPid > 0:
                                theCount += readMessage(pipeCodes[childPid])

                                amount -= 1
                                pipeCodes.pop(childPid)
                                childPid, _ = os.waitpid(-1, os.WNOHANG)
                        except ChildProcessError:
                            pass
                        node1 = Node(entry.path)
                        lst.add(node1)
            obj.close()

        except PermissionError as e:
            pass

        try:
            pid, status = os.wait()
            while pid > 0:
                theCount += readMessage(pipeCodes[pid])

                amount -= 1
                pipeCodes.pop(pid)
                pid, status = os.wait()

        except ChildProcessError:
            pass

    return theCount





signal.signal(signal.SIGINT, signal_handler)
c = list_find('/Users/primus', count)
#

print(c)
