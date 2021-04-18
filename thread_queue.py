import threading
import logging


class QueueNode(object):

    def __init__(self, value, nxt, prev):
        self.value = value
        self.prev = prev
        self.nxt = nxt

    def __repr__(self):
        pval = self.prev and self.prev.value or None
        nval = self.nxt and self.nxt.value or None
        return f'[{repr(pval)}, {self.value}, {repr(nval)}]'


class Queue(object):

    def __init__(self):
        self.front = None
        self.back = None
        # self.producer_lock = threading.Lock()
        # self.consumer_lock = threading.Lock()
        # self.consumer_lock.acquire()
        self._lock = threading.Lock()


    def shift(self, obj, name, index):

        # Apends a new value to the end of the queue.

        logging.debug("%s %s: entered shift()", name, index)
        logging.debug("%s %s: about to acquire the lock", name, index)
        # self.producer_lock.acquire()
        self._lock.acquire()
        logging.debug("%s %s: has the lock", name, index)

        new_elem = QueueNode(obj, None, None)
        logging.debug("%s %s: shift() QueueNode(%s) created", name, index, obj)

        logging.debug("%s %s: QUEUE STATUS -- FRONT: %s, BACK: %s", name, index, self.front, self.back)

        if self.front == None and self.back == None:
            logging.debug("%s %s: entered shift() IF", name, index)
            self.front = new_elem
            self.back = self.front
            logging.debug("%s %s: completed shift() IF", name, index)

        else:
            logging.debug("%s %s: entered shift() ELSE", name, index)
            self.back.nxt = new_elem
            new_elem.prev = self.back
            self.back = new_elem
            logging.debug("%s %s: completed shift() ELSE", name, index)

        logging.debug("%s %s: queued object %s", name, index, obj)
        logging.debug("%s %s: about to release the lock", name, index)
        # self.consumer_lock.release()
        self._lock.release()
        logging.debug("%s %s: released the lock", name, index)


    def count(self):

        # Returns the number of items in the queue.

        if not self.front:

            return 0

        else:
            x = 1
            n = self.front
            while n.nxt != None:
                x += 1
                n = n.nxt
            else:
                return x


    def unshift(self, name, index):

        # Removes the item from the front of the queue and returns it.

        logging.debug("%s %s: about to acquire the lock", name, index)
        # self.consumer_lock.acquire()
        self._lock.acquire()
        logging.debug("%s %s: has the lock", name, index)

        logging.debug("%s %s: QUEUE STATUS -- FRONT: %s, BACK: %s", name, index, self.front, self.back)

        if not self.front:

            logging.debug("%s %s: retrieved no object from queue", name, index)
            logging.debug("%s %s: about to release the lock", name, index)
            # self.producer_lock.release()
            self._lock.release()
            logging.debug("%s %s: released the lock", name, index)

            return None

        elif self.front == self.back:
            n = self.front
            self.front = None
            self.back = None

            logging.debug("%s %s: retrieved %s from queue", name, index, n.value)
            logging.debug("%s %s: about to release the lock", name, index)
            # self.producer_lock.release()
            self._lock.release()
            logging.debug("%s %s: released the lock", name, index)

            return n.value

        else:
            n = self.front
            new_front = self.front.nxt
            new_front.prev = None
            self.front = new_front

            logging.debug("%s %s: retrieved %s from queue", name, index, n.value)
            logging.debug("%s %s: about to release the lock", name, index)
            # self.producer_lock.release()
            self._lock.release()
            logging.debug("%s %s: released the lock", name, index)

            return n.value


    def first(self):

        # Returns a reference for first item in the queue but does not remove it.

        if not self.front:

            return None

        else:

            return self.front.value


    def dump(self):

        # Debugging func that dumps content of the queue.

        if not self.front:

            return None

        elif self.front and not self.front.nxt:

            return f'[{self.front.value}]'

        else:
            dump = f'['
            n = self.front
            while n.nxt != None:
                dump += n.value + ', '
                n = n.nxt
            else:
                dump += n.value + ']'

            return dump


if __name__ == '__main__':

    pass