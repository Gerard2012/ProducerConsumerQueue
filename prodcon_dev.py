from thread_queue import Queue
import concurrent.futures
import logging
import random
import time


def producer(pipeline):

    """Pretend we're getting a message from the network."""

    for index, iteration in enumerate(range(10)):
        obj = random.randint(1, 101)
        logging.info("Producer %s: produced object %s", index, obj)
        logging.debug("Producer %s: about to acquire lock", index)
        pipeline._lock.acquire()
        pipeline.shift(obj, "Producer", index)
        logging.info("Producer %s: added object %s to queue", index, obj)
        pipeline._lock.release()
        logging.debug("Producer %s: released lock", index)
        time.sleep(1)
        logging.info("Producer %s: complete", index)



def consumer(pipeline, index=0):

    """Pretend we're saving a number in the database."""

    pipeline._lock.acquire()

    while pipeline.count() != 0:
        logging.info("Consumer %s: about to check queue for next object", index)
        obj = pipeline.unshift("Consumer", index)
        pipeline._lock.release()
        index += 1
        time.sleep(5)
        logging.info("Consumer %s: consumed object %s", index, obj)

        consumer(pipeline, index)

    else:
        logging.info("Consumer: pipeline is empty")
        pipeline._lock.release()


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Queue()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)