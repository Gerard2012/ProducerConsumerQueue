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
        pipeline.shift(obj, "Producer", index)
        time.sleep(1)
        logging.info("Producer %s: complete", index)

    # Send a sentinel message to tell consumer we're done
    pipeline.shift("END", "Producer", "FINAL")


def consumer(pipeline):
    """Pretend we're saving a number in the database."""
    obj = 0
    index = 0
    while obj is not "END":
        logging.info("Consumer %s: about to check queue for next object", index)
        obj = pipeline.unshift("Consumer", index)
        if obj is not "END":
            time.sleep(5)
            logging.info("Consumer %s: consumed object %s", index, obj)
            index += 1
    else:
        logging.info("Consumer %s: complete, %s", index, obj)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S")
    # logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Queue()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)